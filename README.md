# ⏱️ League Timer

```
  ╔══════════════════════════════════╗
  ║      🎮 League Timer             ║
  ║  Авто-трекер времени для LoL     ║
  ╚══════════════════════════════════╝
```

> 🤖 *Таймер, который сам знает, когда ты в игре*

---

## 📖 О проекте

**League Timer** — десктопное приложение для Windows, которое автоматически отслеживает время, проведённое в **League of Legends**. 

Запустил клиент или игру — таймер пошёл. Вышел — встал на паузу. Всё автоматически, без лишних кликов.

```
✨ Главный принцип: «Поставил и забыл»
```

🔗 **Репозиторий**: https://github.com/mageri9/time_Tracking

---

## 🚀 Возможности

| Фича | Описание |
|------|----------|
| 🎮 **Авто-старт/пауза** | Следит за процессами `LeagueClientUx.exe` и `League of Legends.exe` |
| 🔔 **Уведомления** | Мгновенные оповещения: «Таймер запущен» / «Таймер на паузе» |
| 📊 **Статистика** | Сводка: сегодня / за неделю / всего времени |
| 💾 **Автосохранение** | Сессии сохраняются в `laps_data.json` — ничего не теряется |
| 🖥️ **Системный трей** | Сворачивается в трей, не мешает играть, управление в один клик |
| ⏱️ **Ручной режим** | Старт, пауза, сброс, круги — полный контроль под рукой |
| ✏️ **Умный ввод времени** | Двойной клик → вводи `1h30m`, `90m`, `01:30:00` — парсится всё |
| 🚀 **Флаг `--minimized`** | Старт сразу в трее — идеально для автозагрузки |
| 🔒 **Один экземпляр** | Защита от случайного запуска второй копии |
| 👁️ **LeagueWatcher** | Лёгкий фоновый сторож для автозапуска при входе в систему |
| 📦 **Готовый .exe** | Сборка в один файл через PyInstaller — установка без Python |
| 🧪 **15 unit-тестов** | Покрытие ключевой логики — уверенность в стабильности |

---

## ⚙️ Как это работает

1. Приложение сканирует запущенные процессы через `psutil`
2. При обнаружении `LeagueClientUx.exe` или `League of Legends.exe` → стартует таймер
3. При закрытии процессов → пауза + уведомление
4. Ручное нажатие Start/Pause временно отключает авто-режим до следующей синхронизации

### 🔄 Два режима запуска:

**🎮 LeagueTimer.exe** — полноценное приложение с интерфейсом  
**👁️ LeagueWatcher.exe** — минималистичный фоновый процесс, который запускает таймер только при обнаружении игры

---

## 🎯 Использование

### ▶️ Быстрый старт

```bash
# Обычный запуск
LeagueTimer.exe

# Запуск сразу в трее (для автозагрузки)
LeagueTimer.exe --minimized

# Только сторож (минимальное потребление ресурсов)
LeagueWatcher.exe
```

### 🖱️ Управление

| Действие | Как сделать |
|----------|-------------|
| ▶️ Старт / ⏸️ Пауза | Кнопка в окне **или** правый клик по иконке в трее |
| 🔄 Сброс | Кнопка 🔄 (нажми дважды для подтверждения) |
| ⏱️ Круги / Статистика | Кнопка ⏱️ в интерфейсе |
| ✏️ Ввод времени | Двойной клик по цифрам таймера → введи `1h30m`, `90m`, `01:30:00` |
| 📥 Свернуть в трей | Нажми ❌ в окне приложения |
| 🚪 Полный выход | Правой кнопкой по трею → **Quit** (с автосохранением!) |

### 🧭 Сценарии

```
🎮 "Хочу, чтобы таймер сам включался с игрой"
→ Запусти LeagueWatcher.exe и добавь в автозагрузку

⏱️ "Нужно вручную добавить время за прошлую сессию"
→ Двойной клик по таймеру → введи 2h30m → Enter

🔋 "Хочу, чтобы всё работало с включением ПК"
→ При установке выбери "Добавить LeagueWatcher в автозагрузку"
```

---

## 🛠️ Сборка из исходников

### 📋 Требования
- Windows 10/11
- Python **3.10+** (если собираешь вручную)

### ⚡ Установка в один клик (для не-программистов)

```bash
# Скачай репозиторий и запусти:
setup_and_build.bat
```

Скрипт автоматически:
1. Проверит наличие Python (предложит скачать, если нет)
2. Создаст виртуальное окружение
3. Установит зависимости
4. Соберёт `LeagueTimer.exe` и `LeagueWatcher.exe`
5. **Предложит выбрать**: добавить в автозагрузку `LeagueTimer` или `LeagueWatcher`

### 🔧 Ручная сборка

```bash
# 1. Клонирование
git clone -b league-timer https://github.com/mageri9/time_Tracking.git
cd time_Tracking

# 2. Виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Зависимости
pip install -r requirements.txt

# 4. Запуск из исходников
python -m stopwatch

# 5. Сборка .exe
build_exe.bat
# или вручную:
pyinstaller --noconfirm --noconsole --onefile ^
    --name LeagueTimer ^
    --icon=league_timer.ico ^
    stopwatch/__main__.py
```

### 📦 Зависимости (`requirements.txt`)
```txt
pystray>=0.19.0
Pillow>=10.0.0
psutil>=5.9.0
pyinstaller>=6.0.0
```

---

## 🧪 Тестирование

Проект покрыт **15 unit-тестами** на базе `unittest`.

```bash
# Запустить все тесты
python -m unittest discover -s tests

# Запустить отдельные модули
python -m unittest tests.test_utils
python -m unittest tests.test_statistics
python -m unittest tests.test_monitor
```

✅ Проверяется:
- Парсинг времени (`1h30m`, `90m`, `01:30:00`) — `test_utils.py`
- Расчёт статистики (день/неделя/итого) — `test_statistics.py`
- Логика мониторинга процессов LoL — `test_monitor.py`

---

## 🗂️ Структура проекта

```
time_Tracking/
├── stopwatch/
│   ├── __main__.py      # Точка входа + защита от дублей
│   ├── models.py        # Данные: состояние таймера, сессии, JSON
│   ├── controllers.py   # Бизнес-логика, статистика, авто-режим
│   ├── views.py         # GUI на Tkinter
│   ├── theme.py         # Цветовая схема (27+ констант)
│   ├── tray.py          # Интеграция с системным треем (pystray)
│   ├── monitor.py       # Мониторинг процессов LoL через psutil
│   ├── lock.py          # Lock-file для предотвращения повторных запусков
│   └── utils.py         # Парсинг времени, форматирование, хелперы
├── tests/
│   ├── test_utils.py        # Тесты парсинга и утилит
│   ├── test_statistics.py   # Тесты расчёта статистики
│   └── test_monitor.py      # Тесты мониторинга процессов
├── requirements.txt
├── build_exe.bat            # Быстрая сборка .exe
├── setup_and_build.bat      # Полная установка с авто-поиском Python
├── league_timer.ico         # Иконка приложения
├── README.md
└── .gitignore
```

---

## 🤝 Участие в разработке

Баги, идеи, улучшения — приветствуются! 🙌

1. Форкни репозиторий
2. Создай ветку: `git checkout -b feature/cool-idea`
3. Закоммить изменения: `git commit -m '✨ Add cool feature'`
4. Запушь: `git push origin feature/cool-idea`
5. Открой Pull Request

> 💡 Перед отправкой убедись, что тесты проходят: `python -m unittest`

---

## 📜 Лицензия

Распространяется под лицензией **MIT**.

```
MIT License

Copyright (c) 2026 Alexander Evgenievich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🛠️ Стек технологий

- **Python 3.10+**
- **tkinter** — графический интерфейс
- **pystray** — интеграция с системным треем
- **psutil** — мониторинг процессов
- **Pillow** — работа с иконками
- **PyInstaller** — сборка в standalone .exe

---

```
   ╭──────────────────────────────╮
   │  💜 GLHF & Happy Timing!     │
   │  Сделано с любовью к коду    │
   │  и уважению к твоему времени │
   ╰──────────────────────────────╯
```

> 📬 Вопросы, предложения, багрепорты — добро пожаловать в [Issues](https://github.com/mageri9/time_Tracking/issues) или пиши напрямую автору.