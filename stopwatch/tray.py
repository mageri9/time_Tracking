"""
Менеджер системного трея для League Timer.

Запускает pystray в отдельном daemon-потоке,
общается с основным (tkinter) потоком через thread-safe очередь.
"""
from __future__ import annotations
import queue
import threading


from PIL import Image, ImageDraw
import pystray

from .theme import COLORS

ICON_SIZE = 32

def _generate_icon() -> Image.Image:
    """Генерируем иконку: золотой кружок с жирной буквой L."""
    img = Image.new("RGBA", (ICON_SIZE, ICON_SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    padding = 2

    draw.ellipse(
        [padding, padding, ICON_SIZE - padding, ICON_SIZE - padding],
        fill=COLORS["info_fg"],
    )

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        draw.text(
            (ICON_SIZE // 2 + dx, ICON_SIZE // 2 + dy),
            "L",
            fill=COLORS["bg_dark"],
            anchor="mm",
        )

    draw.text(
        (ICON_SIZE // 2, ICON_SIZE // 2),
        "L",
        fill=COLORS["bg_dark"],
        anchor="mm",
    )

    return img

CMD_SHOW = "SHOW"
CMD_QUIT = "QUIT"
CMD_START = "START"

class TrayManager:
    """
    Управляет иконкой в системном трее.

    Запускается в отдельном потоке, не блокирует tkinter.
    Команды (показать окно / выйти) кладёт в очередь,
    основной поток их разбирает через root.after().
    """
    def __init__(self, queue: queue.Queue) -> None:
        self.queue = queue
        self.icon: pystray.Icon | None = None
        self._thread: threading.Thread | None = None

    # --- Публичные методы (вызываются из основного потока) ---

    def start(self) -> None:
        """Запускает pystray в фоновом daemon-потоке."""
        if self._thread is not None:
            return

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self.icon is not None:
            self.icon.stop()
            self.icon = None

    def notify(self, message: str) -> None:
        """Показывает всплывающее уведомление над треем."""
        if self.icon is not None:
            self.icon.notify(message, title="League Timer")


    # --- Внутренние ---

    def _run(self) -> None:
        """Точка входа для потока pystray."""
        # Пробуем загрузить иконку из файла, иначе генерируем
        import os
        icon_path = os.path.join(os.path.dirname(__file__), "..", "league_timer.ico")
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
        else:
            image = _generate_icon()

        menu = pystray.Menu(
            pystray.MenuItem("Start/Pause", self._on_start),
            pystray.MenuItem("Show", self._on_show, default=True),
            pystray.MenuItem("Quit", self._on_quit),
        )
        self.icon = pystray.Icon(
            name="League Timer",
            title="League Timer",
            icon=image,
            menu=menu,
        )
        self.icon.run()


    def _on_show(self) -> None:
        """Пользователь нажал "Показать" в меню трея."""
        self.queue.put(CMD_SHOW)

    def _on_quit(self) -> None:
        """Пользователь нажал "Выход" в меню трея."""
        self.queue.put(CMD_QUIT)

    def _on_start(self) -> None:
        """Пользователь нажал Старт/Пауза в меню трея."""
        self.queue.put(CMD_START)

    def set_tooltip(self, text: str) -> None:
        """Меняет тултип у иконки в трее."""
        if self.icon is not None:
            self.icon.title = text