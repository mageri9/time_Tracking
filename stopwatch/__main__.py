import queue
import tkinter as tk

from stopwatch.controllers import StopwatchController
from stopwatch.tray import CMD_QUIT, CMD_SHOW, CMD_START, TrayManager
from stopwatch.views import StopwatchView


def main() -> None:
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

    root.deiconify()
    root.mainloop()



if __name__ == "__main__":
    main()

