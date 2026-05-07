import queue
import sys
import tkinter as tk
import os

from stopwatch.controllers import StopwatchController
from stopwatch.tray import CMD_QUIT, CMD_SHOW, CMD_START, TrayManager
from stopwatch.views import StopwatchView
from PIL import Image, ImageTk
import ctypes


def main() -> None:

    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Timer.TimerApp")
    except Exception:
        pass

    start_minimized = "--minimized" in sys.argv

    cmd_queue: queue.Queue = queue.Queue()
    tray = TrayManager(cmd_queue)

    root = tk.Tk()

    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    icon_path = os.path.join(base_dir, "_timer.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
        root.wm_iconbitmap(icon_path)

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

