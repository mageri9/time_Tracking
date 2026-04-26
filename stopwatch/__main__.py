import atexit
import queue
import sys
import tkinter as tk

from stopwatch.controllers import StopwatchController
from stopwatch.tray import CMD_QUIT, CMD_SHOW, CMD_START, TrayManager
from stopwatch.views import StopwatchView
from stopwatch.lock import already_running, create_lock, remove_lock


def main() -> None:
    if already_running():
        sys.exit(0)

    create_lock()
    atexit.register(remove_lock)

    start_minimized = "--minimized" in sys.argv

    cmd_queue: queue.Queue = queue.Queue()
    tray = TrayManager(cmd_queue)

    root = tk.Tk()

    controller = StopwatchController("laps_data.json")
    view = StopwatchView(root, controller, tray, cmd_queue)

    tray._view = view
    tray.start()

    def process_queue() -> None:
        try:
            while True:
                cmd = cmd_queue.get_nowait()
                if cmd == CMD_SHOW:
                    view.show_window()
                elif cmd == CMD_QUIT:
                    view.quit_app()
                elif cmd == CMD_START:
                    view.toggle_start_pause()
        except queue.Empty:
            pass
        root.after(100, process_queue)

    process_queue()
    if start_minimized:
        root.withdraw()
    else:
        root.deiconify()

    root.mainloop()



if __name__ == "__main__":
    main()

