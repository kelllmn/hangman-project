# Игра «Виселица» — учебный проект

Десктопная игра «Виселица» на PyQt6/Python с интегрированной системой обучающих подсказок по Python.

---
## Состояние проекта

**Финальная версия** (ветка `review/final`), включающая:
- Полную игровую логику
- Систему обучающих подсказок по Python (18 вопросов)
- UML-диаграммы (Use Case, Activity, Class)
- Модульные тесты
- Аналитическую документацию

> Все промежуточные ветки (`ba/game-description`, `feature/architecture`, `feature/programmists`, `test/hint-system-validation`) слиты в `review/final`.

---
## Структура проекта

```
review/final/
├── ba/
│   └── analytic_doc.md              # Аналитическая документация 
├── architecture/
│   ├── hangmanUseCase.png           # Use Case диаграмма
│   ├── activity.png                 # Диаграмма активности
│   ├── class.png                    # Диаграмма классов
│   ├── *.mdj                        # Исходники диаграмм (StarUML)
├── Hangman-on-the-Field-of-Miracles-main/
│   ├── main.py                      # Точка входа — запускать отсюда
│   ├── requirements.txt
│   ├── assets/
│   │   └── data/
│   │       ├── words.json           # База русских слов
│   │       └── hangman_stages.json  # ASCII-стадии виселицы
│   └── src/
│       ├── core/
│       │   ├── game_logic.py        # Логика игры (create/update hidden word)
│       │   └── data_loader.py       # Загрузка JSON и стилей
│       └── ui/
│           ├── game_window.py       # Игровой экран + кнопка подсказки 
│           ├── hint_dialog.py       # Диалог подсказки (choice/input/code) 
│           ├── main_menu.py         # Главное меню
│           ├── main_window.py       # Корневой виджет-стек
│           └── settings_window.py   # Настройки
├── educational/
│   ├── hint_system.py               # Класс QuestionBank
│   └── questions.json               # 18 вопросов по Python 
└── tests/
    ├── test_hint_system.py          # Тесты QuestionBank 
    └── test_game_logic.py           # Тесты игровой логики 
```

---


## Установка и запуск

### Требования

- Python 3.10+
- PyQt6

### Установка зависимостей

```bash
pip install PyQt6
```

### Запуск игры

```bash
# Перейти в папку с игрой
cd review/final/Hangman-on-the-Field-of-Miracles-main
# Запустить
python main.py
```

> **Важно:** запускать именно из папки `Hangman-on-the-Field-of-Miracles-main/`, иначе относительные пути к `assets/` не найдут нужные файлы.

### Запуск тестов

```bash
# Из корня review/final/
pip install pytest
pytest tests/ -v
```

---

## Система подсказок

Кнопка **«💡 Подсказка»** на игровом экране открывает диалог с вопросом по Python среднего уровня. Три типа вопросов:

- **choice** — выбор из 4 вариантов
- **input** — ввод ответа текстом
- **code** — дополнение фрагмента кода (вставить пропущенное слово вместо `___`)

За правильный ответ открывается случайная ещё не угаданная буква. За неверный — кнопка блокируется до следующего раунда.

## Сборка

Все ветки (`ba/game-description`, `feature/architecture`, `feature/programmists`, `test/hint-system-validation`) слиты в `review/final`. Для запуска используйте финальную версию.
