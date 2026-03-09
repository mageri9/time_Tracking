import tkinter as tk

from .controllers import StopwatchController
from .views import StopwatchView


def main() -> None:
    """Точка входа для запуска секундомера."""
    root = tk.Tk()
    controller = StopwatchController()
    StopwatchView(root, controller)
    root.mainloop()


if __name__ == "__main__":
    main()

