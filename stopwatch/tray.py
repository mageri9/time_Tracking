"""
Менеджер системного трея для League Timer.

Запускает pystray в отдельном daemon-потоке,
общается с основным (tkinter) потоком через thread-safe очередь.
"""
from __future__ import annotations
import queue
import threading
from typing import Callable

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

    # --- Внутренние ---

    def _run(self) -> None:
        """Точка входа для потока pystray (свой event loop)."""
        image = _generate_icon()

        menu = pystray.Menu(
            pystray.MenuItem("Показать", self._on_show, default=True),
            pystray.MenuItem("Выход", self._on_quit),
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