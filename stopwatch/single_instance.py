"""
Механизм единственного экземпляра с возможностью активации существующего окна.
"""
import os
import sys
import socket
import tempfile
from pathlib import Path
import threading
import time


class SingleInstance:
    """Обеспечивает запуск только одного экземпляра с активацией существующего."""

    def __init__(self, app_name="Timer", port=49152):
        self.app_name = app_name
        self.port = port
        self.socket = None
        self.listener_thread = None
        self.on_activate_callback = None

    def register(self, on_activate=None) -> bool:
        """Регистрирует приложение как единственный экземпляр.

        Args:
            on_activate: Функция, вызываемая при попытке запуска второго экземпляра

        Returns:
            True если приложение должно запуститься, False если уже запущено
        """
        self.on_activate_callback = on_activate

        # Пробуем создать сокет для прослушивания
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if os.name != "nt":
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('127.0.0.1', self.port))
            self.socket.listen(5)

            # Запускаем слушатель в фоновом потоке
            self.listener_thread = threading.Thread(target=self._listen, daemon=True)
            self.listener_thread.start()

            return True  # Первый экземпляр

        except socket.error:
            # Порт занят - приложение уже запущено
            self._send_activate_signal()
            return False  # Второй экземпляр

    def _send_activate_signal(self):
        """Отправляет сигнал существующему приложению."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', self.port))
            sock.send(b"ACTIVATE")
            sock.close()
        except Exception:
            pass

    def _listen(self):
        """Слушает входящие сигналы от других экземпляров."""
        while True:
            try:
                conn, addr = self.socket.accept()
                data = conn.recv(1024)
                if data == b"ACTIVATE" and self.on_activate_callback:
                    # Вызываем callback в главном потоке
                    threading.Thread(
                        target=self.on_activate_callback,
                        daemon=True
                    ).start()
                conn.close()
            except Exception:
                break

    def cleanup(self):
        """Освобождает ресурсы."""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass