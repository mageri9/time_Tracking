import tkinter as tk
import time

class Stopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("Секундомер")
        self.root.geometry("300x400")
        self.root.resizable(False, False)

        # Переменные состояния
        self.running = False          # идёт ли отсчёт
        self.start_time = 0.0         # время запуска (time.time)
        self.elapsed_time = 0.0        # накопленное время (при паузах)
        self.lap_count = 0             # счётчик кругов

        # Дисплей времени
        self.time_label = tk.Label(
            root,
            text="00:00.00",
            font=("Courier New", 41, "bold"),  # моноширинный шрифт
            bg="#1a1a1a",  # темно-серый фон
            fg="#b3ff8c",  # Pastel Lime
            relief="sunken",  # утопленный эффект
            bd=20,  # толщина рамки
        )
        self.time_label.pack()

        # Кнопки управления
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        self.start_btn = tk.Button(btn_frame, text="Старт", width=8, command=self.start)
        self.start_btn.grid(row=0, column=0, padx=5)

        self.stop_btn = tk.Button(btn_frame, text="Стоп", width=8, command=self.stop, state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)

        self.reset_btn = tk.Button(btn_frame, text="Сброс", width=8, command=self.reset)
        self.reset_btn.grid(row=0, column=2, padx=5)

        # Кнопка круга
        self.lap_btn = tk.Button(root, text="Круг", width=10, command=self.lap, state=tk.DISABLED)
        self.lap_btn.pack(pady=10)

        # Список для отображения кругов
        self.lap_listbox = tk.Listbox(root, height=10)
        self.lap_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0,10))

        # Запуск обновления времени
        self.update_display()

    def start(self):
        """Запускает секундомер (или продолжает после паузы)"""
        if not self.running:
            self.running = True
            self.start_time = time.time() - self.elapsed_time   # корректируем старт с учётом уже накопленного времени
            # Обновляем состояние кнопок
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.lap_btn.config(state=tk.NORMAL)
            1

    def stop(self):
        """Останавливает секундомер (пауза)"""
        if self.running:
            self.running = False
            self.elapsed_time = time.time() - self.start_time   # запоминаем накопленное время
            # Обновляем состояние кнопок




    def reset(self):
        """Сбрасывает секундомер и все круги"""
        self.running = False
        self.elapsed_time = 0.0
        self.lap_count = 0
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.lap_btn.config(state=tk.DISABLED)
        self.lap_listbox.delete(0, tk.END)
        self.update_display()   # сразу обновим метку

    def lap(self):
        """Фиксирует время круга"""
        if self.running:
            self.lap_count += 1
            current = time.time() - self.start_time
            minutes = int(current // 60)
            seconds = int(current % 60)
            hundredths = int((current * 100) % 100)
            lap_time = f"{minutes:02d}:{seconds:02d}.{hundredths:02d}"
            self.lap_listbox.insert(tk.END, f"Круг {self.lap_count}: {lap_time}")
            self.lap_listbox.see(tk.END)   # прокрутить вниз

    def update_display(self):
        """Обновляет метку времени (вызывается каждые 50 мс)"""
        if self.running:
            # текущее время с учётом старта
            current = time.time() - self.start_time
            minutes = int(current // 60)
            seconds = int(current % 60)
            hundredths = int((current * 100) % 100)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}.{hundredths:02d}")
        else:
            # показываем накопленное время (если не running)
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            hundredths = int((self.elapsed_time * 100) % 100)
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}.{hundredths:02d}")

        # повторяем обновление через 50 мс
        self.root.after(50, self.update_display)


if __name__ == "__main__":
    root = tk.Tk()
    app = Stopwatch(root)
    root.mainloop()
