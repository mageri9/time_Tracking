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


def reset(self):
    current = self.current_time() if self.running else self.elapsed_time

    if current == 0 and self.saved_time:
        self.elapsed_time = self.saved_time
        self.saved_time = 0
        self.reset_btn.config(bg="#2B2B2B")
        self.set_info("✨ Время восстановлено")
    elif current > 0:
        self.saved_time = current
        if self.running:
            self.stop()
        self.elapsed_time = 0
        self.reset_btn.config(bg="#666666")
        self.set_info("🔄 Нажми для отмены")
    else:
        self.set_info("✨ Нет времени\n"
                      "       для сброса")

    self.update_display()

    def current_time(self):
        """Текущее время секундомера"""
        if self.running:
            return time.time() - self.start_time
        return self.elapsed_time

    def reset(self):
        current = self.current_time() if self.running else self.elapsed_time

        if current == 0 and self._undo:
            self.elapsed_time = self._undo
            self._undo = 0
        elif current > 0:
            self._undo = current
            if self.running:
                self.stop()
            self.elapsed_time = 0
        else:
            return

        self.update_display()