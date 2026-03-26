import tkinter as tk
from stopwatch.controllers import StopwatchController
from stopwatch.views import StopwatchView


def main() -> None:
    root = tk.Tk()
    root.withdraw()

    controller = StopwatchController("laps_data.json")

    root.deiconify()
    StopwatchView(root, controller)
    root.mainloop()


if __name__ == "__main__":
    main()

