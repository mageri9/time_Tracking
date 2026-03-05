import tkinter as tk
import time
import json
import os


class Stopwatch:
    """Основной класс секундомера"""

    def __init__(self, root):
        """Инициализация главного окна и переменных"""
        self.root = root
        self.root.title("Секундомер")
        self.root.geometry("300x300")
        self.root.resizable(False, False)

        # Переменные состояния
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.laps = []
        self.data_file = "laps_data.json"
        self.hours = 0
        self.saved_time = 0.0

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
            command=self.toggle_start_pause
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
            command=self.reset
        )
        self.reset_btn.grid(row=0, column=1, padx=5)

        # Кнопка Круг
        self.lap_btn = tk.Button(
            btn_frame,
            text="⏱️",
            bg="#2B2B2B",
            fg="#9bfa9b",
            bd=6,
            font=("Arial", 30),
            highlightbackground="#E0E0E0",
            highlightthickness=2,
            activebackground="#9FD6F0",
            width=8,
            command=self.lap,
            state=tk.DISABLED
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
            anchor="w"
        )
        self.info_label.pack(fill="both", expand=True, padx=0, pady=0)

        self.load_laps()
        self.update_display()

    def set_info(self, message):
        """Показывает сообщение в инфопанели"""
        self.info_label.config(text=f" {message}")

    def toggle_start_pause(self):
        """Переключает между состояниями запущено/пауза"""
        if self.running:
            self.stop()
            button_text, button_color = "▶", "#2D2D2D"
        else:
            self.start()
            button_text, button_color = "⏸", "#666666"
            self.reset_btn.config(bg="#2D2D2D")

        self.set_info("✨")
        self.start_btn.config(text=button_text, bg=button_color)
        self.lap_btn.config(state=tk.NORMAL)
        self.start_btn.config(state=tk.NORMAL)
        self.reset_btn.config(state=tk.NORMAL)

    def start(self):
        """Запускает секундомер (или продолжает после паузы)"""
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time

    def stop(self):
        """Останавливает секундомер (пауза)"""
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time

    def reset(self):
        """Сбрасывает секундомер и все круги с возможностью отмены"""
        current_time = (
            time.time() - self.start_time if self.running else self.elapsed_time
        )

        if current_time == 0.0 and self.saved_time != 0.0:
            # Второе нажатие — возвращаем сохранёнку
            self.elapsed_time = self.saved_time
            self.saved_time = 0.0
            self.reset_btn.config(bg="#2B2B2B")
            self.set_info("✨ Время восстановлено")
        elif current_time > 0:
            # Первое нажатие — сохраняем текущее время
            self.saved_time = current_time
            self.running = False
            self.elapsed_time = 0.0
            self.reset_btn.config(bg="#666666")
            self.set_info("🔄 Нажми для отмены")
        else:
            # Время 0 и сохранёнки нет — просто сброс
            self.set_info("✨ Нет времени\n"
                          "       для сброса")

        self.start_btn.config(text="▶", bg="#2B2B2B")
        self.update_display()

    def clear(self):
        """Сбрасывает секундомер и все круги"""
        self.running = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.update_display()

    def lap(self):
        """Записывает круг или показывает статистику"""
        if not self.running and len(self.laps) > 0:
            total = sum(self.laps)
            avg = total / len(self.laps)
            self.set_info(
                f"Всего: {self.format_time(total, include_hours=True)}\n"
                f"В среднем: {self.format_time(avg, include_hours=True)}"
            )
            return

        current = time.time() - self.start_time
        self.laps.append(current)
        self.save_laps()
        self.set_info(f"Круг {self.format_time(current)}")
        self.clear()
        self.start_btn.config(text="▶", bg="#2B2B2B")

    def save_laps(self):
        """Сохраняет круги в JSON-файл"""
        with open(self.data_file, "w") as f:
            json.dump(self.laps, f, indent=2)

    def load_laps(self):
        """Загружает круги из JSON-файла"""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                self.laps = json.load(f)
        else:
            self.laps = []
            self.set_info("✨ Новый файл")

    def format_time(self, amount, include_hours=False):
        """Форматирует время в минуты:секунды.сотые"""
        hours = int(amount // 3600)
        minutes = int((amount % 3600) // 60)
        seconds = int(amount % 60)
        hundredths = int((amount * 100) % 100)

        if include_hours:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"

    def update_display(self):
        """Обновляет метку времени каждые 50 мс"""
        if self.running:
            current = time.time() - self.start_time
            self.time_label.config(text=f"{self.format_time(current)}")
            h_current = int(current // 3600)

            if h_current > self.hours:
                self.hours = h_current
                self.set_info(f"Часов прошло: {self.hours}")
        else:
            self.time_label.config(text=f"{self.format_time(self.elapsed_time)}")

        self.root.after(50, self.update_display)


if __name__ == "__main__":
    root = tk.Tk()
    app = Stopwatch(root)
    root.mainloop()