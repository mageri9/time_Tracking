import tkinter as tk
from tkinter import messagebox
from typing import TYPE_CHECKING

from .controllers import StopwatchController
from .theme import COLORS
from .utils import format_time
from .monitor import is_league_running

if TYPE_CHECKING:
    import queue
    from .tray import TrayManager


class StopwatchView:
    """GUI-обёртка над контроллером секундомера."""

    def __init__(
            self,
            root: tk.Tk,
            controller: StopwatchController,
            tray: "TrayManager",
            cmd_queue: "queue.Queue",
    ) -> None:
        self.root = root
        self.controller = controller
        self.tray = tray
        self.cmd_queue = cmd_queue
        self.auto_mode = True

        self.root.title("League Timer")
        self.root.geometry("300x300")
        self.root.resizable(False, False)
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        # Дисплей времени
        self.time_label = tk.Label(
            root,
            text="00:00.00",
            font=("Courier New", 41, "bold"),
            bg=COLORS["timer_bg"],
            fg=COLORS["timer_fg"],
            relief="sunken",
            bd=20,
        )
        self.time_label.pack()
        # Делаем метку времени кликабельной
        self.time_label.bind("<Double-Button-1>", self.start_edit)

        # Рамка для кнопок
        btn_frame = tk.Frame(root, bg=COLORS["panel_bg"], height=50)
        btn_frame.pack(fill="x")
        btn_frame.pack_propagate(False)

        # Кнопка Старт/Пауза
        self.start_btn = tk.Button(
            btn_frame,
            text="▶",
            bg=COLORS["button_idle"],
            fg=COLORS["button_fg"],
            bd=6,
            font=("Arial", 30),
            highlightbackground=COLORS["button_highlight"],
            activebackground=COLORS["active_start"],
            highlightthickness=2,
            width=8,
            command=self.toggle_start_pause,
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        # Кнопка Сброс
        self.reset_btn = tk.Button(
            btn_frame,
            text="🔄",
            bg=COLORS["button_idle"],
            fg=COLORS["button_fg"],
            font=("Arial", 30),
            bd=6,
            highlightbackground=COLORS["button_highlight"],
            highlightthickness=2,
            activebackground=COLORS["active_reset"],
            width=8,
            command=self.reset,
        )
        self.reset_btn.grid(row=0, column=1, padx=5)

        # Кнопка Круг
        self.lap_btn = tk.Button(
            btn_frame,
            text="⏱️",
            bg=COLORS["button_idle"],
            fg=COLORS["button_fg"],
            bd=6,
            font=("Arial", 30),
            highlightbackground=COLORS["button_highlight"],
            highlightthickness=2,
            activebackground=COLORS["active_lap"],
            width=8,
            command=self.lap,
        )
        self.lap_btn.grid(row=0, column=2, padx=5)

        # Настройка колонок для равномерного распределения
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)

        # Информационная панель
        self.info_label = tk.Label(
            root,
            font=("Arial", 13),
            bg=COLORS["info_bg"],
            fg=COLORS["info_fg"],
            relief="sunken",
            bd=20,
            anchor="w",
            justify="left",
        )
        self.info_label.pack(fill="both", expand=True, padx=0, pady=0)

        # Сообщение в зависимости от наличия кругов
        if self.controller.state.has_laps:
            self.set_info("Нажми ⏱️\nдля просмотра статистики")
        else:
            self.set_info(" Новый файл")

        self.update_display()

        self.root.after(500, self.check_process)

    # --- Служебные методы GUI ---

    def set_info(self, message: str) -> None:
        """Показывает сообщение в инфопанели."""
        self.info_label.config(text=f"✨ {message}")

    def hide_window(self) -> None:
        """Сворачивает окно в трей вместо закрытия."""
        self.root.withdraw()

    def check_process(self) -> None:
        """Авто-старт/пауза по наличию процесса Лиги (раз в 3 сек)."""
        league_running = is_league_running()

        if not self.auto_mode:
            if league_running == self.controller.state.running:
                self.auto_mode = True

        if self.auto_mode:
            if league_running and not self.controller.state.running:
                self.controller.start()
                self.start_btn.config(text="⏸")
                self.set_info("LoL запущен.✨")
                self.tray.notify("Таймер запущен")

            elif not league_running and self.controller.state.running:
                self.controller.stop()
                self.start_btn.config(text="▶")
                self.set_info("LoL закрыт✨")
                self.tray.notify("Таймер на паузе")

        self.root.after(3000, self.check_process)


    def show_window(self) -> None:
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def quit_app(self) -> None:
        if self.controller.state.running:
            self.controller.stop()
        self.tray.stop()
        self.root.destroy()

    # --- Обработчики кнопок ---

    def toggle_start_pause(self) -> None:
        """Переключает между состояниями запущено/пауза."""
        self.auto_mode = False

        if self.controller.state.running:
            self.controller.stop()
            self.start_btn.config(text="▶", bg=COLORS["button_idle"])
        else:
            self.controller.start()
            self.start_btn.config(text="⏸", bg=COLORS["button_paused"])
            self.reset_btn.config(bg=COLORS["button_idle"])
            self.lap_btn.config(bg=COLORS["button_idle"])

        self.set_info("")

    def reset(self) -> None:
        """Сбрасывает секундомер и все круги с возможностью отмены."""
        result = self.controller.reset()

        if result == "restored":
            self.reset_btn.config(bg=COLORS["button_idle"])
            self.set_info(" Время восстановлено")
        elif result == "saved":
            self.reset_btn.config(bg=COLORS["button_paused"])
            self.lap_btn.config(bg=COLORS["button_idle"])
            self.set_info("🔄 Нажми для отмены")
        else:
            self.set_info(" Нет времени\n       для сброса")

        self.start_btn.config(text="▶", bg=COLORS["button_idle"])
        self.update_display()

    def clear(self) -> None:
        """Сбрасывает секундомер и все круги без сохранения."""
        self.controller.clear()
        self.update_display()

    def lap(self) -> None:
        """Записывает круг или показывает статистику."""
        result = self.controller.lap()

        if result["type"] == "stats":
            today = self.controller.get_stats_today()
            week = self.controller.get_stats_week()
            total = self.controller.get_stats_total()

            self.set_info(
                f"Сегодня:  {format_time(today, include_hours=True)}\n"
                f"✨Неделя:   {format_time(week, include_hours=True)}\n"
                f"✨Всего:    {format_time(total, include_hours=True)}"
            )
        else:
            self.lap_btn.config(bg=COLORS["button_paused"])
            elapsed = result["elapsed"]
            self.set_info(
                f"Записано {format_time(elapsed, include_hours=True)}\n"
                f"Нажми ⏱️ для статистики"
            )
            self.start_btn.config(text="▶", bg=COLORS["button_idle"])

    # --- Редактирование времени ---

    def start_edit(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Начинает редактирование времени."""
        self.edit_entry = tk.Entry(
            self.root,
            font=("Arial", 48),
            bg=COLORS["timer_bg"],
            fg=COLORS["timer_fg"],
            insertbackground=COLORS["border"],
            borderwidth=0,
            justify="center",
        )

        current = self.time_label.cget("text")
        self.edit_entry.insert(0, current)

        self.edit_entry.place(
            x=self.time_label.winfo_x(),
            y=self.time_label.winfo_y(),
            width=self.time_label.winfo_width(),
            height=self.time_label.winfo_height(),
        )

        self.edit_entry.focus()
        self.edit_entry.bind("<Return>", self.finish_edit)
        self.edit_entry.bind("<FocusOut>", self.finish_edit)

    def finish_edit(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Завершает редактирование."""
        try:
            new_time = self.edit_entry.get()
            self.controller.set_elapsed_from_str(new_time)
            self.update_display()
        except ValueError:
            self.set_info(" Неверный формат времени")

        self.edit_entry.destroy()

    # --- Обновление дисплея ---

    def update_display(self) -> None:
        """Обновляет метку времени каждые 50 мс."""
        current = self.controller.state.current_time

        def format_for_display(amount: float) -> str:
            # До часа показываем ММ:СС.сотые, после часа — ЧЧ:ММ:СС
            if int(amount // 3600) > 0:
                return format_time(amount, include_hours=True)
            return format_time(amount)

        if self.controller.state.running:
            self.time_label.config(text=format_for_display(current))
        else:
            self.time_label.config(
                text=format_for_display(self.controller.state.elapsed_time)
            )
        current_text = self.time_label.cget("text")
        self.tray.set_tooltip(current_text)
        self.root.after(50, self.update_display)

