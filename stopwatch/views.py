import tkinter as tk
from tkinter import messagebox

from .controllers import StopwatchController
from .utils import format_time


class StopwatchView:
    """GUI-обёртка над контроллером секундомера."""

    def __init__(self, root: tk.Tk, controller: StopwatchController) -> None:
        self.root = root
        self.controller = controller

        self.root.title("Секундомер")
        self.root.geometry("300x350")
        self.root.resizable(False, False)
        # Подтверждение перед закрытием окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Дисплей времени
        self.time_label = tk.Label(
            root,
            text="00:00.00",
            font=("Courier New", 41, "bold"),
            bg="#1a1a1a",
            fg="#9bfa9b",
            relief="sunken",
            bd=20,
        )
        self.time_label.pack()
        # Делаем метку времени кликабельной
        self.time_label.bind("<Double-Button-1>", self.start_edit)

        # Рамка для кнопок
        btn_frame = tk.Frame(root, bg="#333333", height=50)
        btn_frame.pack(fill="x")
        btn_frame.pack_propagate(False)

        # Кнопка Старт/Пауза
        self.start_btn = tk.Button(
            btn_frame,
            text="▶",
            bg="#2B2B2B",
            fg="#9bfa9b",
            bd=6,
            font=("Arial", 30),
            highlightbackground="#E0E0E0",
            highlightthickness=2,
            activebackground="#d1fac3",
            width=8,
            command=self.toggle_start_pause,
        )
        self.start_btn.grid(row=0, column=0, padx=5, pady=5)

        # Кнопка Сброс
        self.reset_btn = tk.Button(
            btn_frame,
            text="🔄",
            bg="#2B2B2B",
            fg="#9bfa9b",
            font=("Arial", 30),
            bd=6,
            highlightbackground="#E0E0E0",
            highlightthickness=2,
            activebackground="#fa9191",
            width=8,
            command=self.reset,
        )
        self.reset_btn.grid(row=0, column=1, padx=5)

        # Кнопка Круг
        self.lap_btn = tk.Button(
            btn_frame,
            text="⏱️",
            bg="#666666",
            fg="#9bfa9b",
            bd=6,
            font=("Arial", 30),
            highlightbackground="#E0E0E0",
            highlightthickness=2,
            activebackground="#9FD6F0",
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
            font=("Arial", 16),
            bg="#1a1a1a",
            fg="#9bfa9b",
            relief="sunken",
            bd=20,
            anchor="w",
        )
        self.info_label.pack(fill="both", expand=True, padx=0, pady=0)

        # Сообщение в зависимости от наличия кругов
        if self.controller.state.has_laps:
            self.set_info("Нажми ⏱️\nдля просмотра статистики")
        else:
            self.set_info(" Новый файл")

        self.update_display()

    # --- Служебные методы GUI ---

    def set_info(self, message: str) -> None:
        """Показывает сообщение в инфопанели."""
        self.info_label.config(text=f"✨ {message}")

    def on_close(self) -> None:
        """Обработка попытки закрыть окно."""
        if self.controller.state.running:
            should_quit = messagebox.askokcancel(
                "Закрыть секундомер?",
                "Секундомер сейчас идёт.\n"
                "Если закрыть окно, отсчёт прервётся.\n\n"
                "Точно выйти?",
                parent=self.root,
            )
            if not should_quit:
                return

        self.root.destroy()

    # --- Обработчики кнопок ---

    def toggle_start_pause(self) -> None:
        """Переключает между состояниями запущено/пауза."""
        if self.controller.state.running:
            self.controller.stop()
            button_text, button_color = "▶", "#2B2B2B"
        else:
            self.controller.start()
            button_text, button_color = "⏸", "#666666"
            self.reset_btn.config(bg="#2B2B2B")
            self.lap_btn.config(bg="#2B2B2B")

        self.set_info("✨✨")
        self.start_btn.config(text=button_text, bg=button_color)

    def reset(self) -> None:
        """Сбрасывает секундомер и все круги с возможностью отмены."""
        result = self.controller.reset()

        if result == "restored":
            self.reset_btn.config(bg="#2B2B2B")
            self.set_info(" Время восстановлено")
        elif result == "saved":
            self.reset_btn.config(bg="#666666")
            self.lap_btn.config(bg="#2B2B2B")
            self.set_info("🔄 Нажми для отмены")
        else:
            self.set_info(" Нет времени\n       для сброса")

        self.start_btn.config(text="▶", bg="#2B2B2B")
        self.update_display()

    def clear(self) -> None:
        """Сбрасывает секундомер и все круги без сохранения."""
        self.controller.clear()
        self.update_display()

    def lap(self) -> None:
        """Записывает круг или показывает статистику."""
        result = self.controller.lap()

        if result["type"] == "stats":
            total = result["total"]
            avg = result["avg"]
            self.set_info(
                f"       Всего: {format_time(total, include_hours=True)}\n"
                f"✨В среднем: {format_time(avg, include_hours=True)}"
            )
        else:
            self.lap_btn.config(bg="#666666")
            elapsed = result["elapsed"]
            self.set_info(
                f"Записано {format_time(elapsed, include_hours=True)}\n"
                f"Нажми ⏱️ для статистики"
            )
            self.start_btn.config(text="▶", bg="#2B2B2B")

    # --- Редактирование времени ---

    def start_edit(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        """Начинает редактирование времени."""
        self.edit_entry = tk.Entry(
            self.root,
            font=("Arial", 48),
            bg="#1a1a1a",
            fg="#9bfa9b",
            insertbackground="#9bfa9b",
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

        self.root.after(50, self.update_display)

