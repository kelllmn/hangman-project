# Игра «Виселица» — учебный проект

Десктопная игра «Виселица» на PyQt6/Python с интегрированной системой обучающих подсказок по Python.

---

## Структура проекта

```
hangman-project/
├── ba/
│   └── analytic_doc.md              # Аналитическая документация (ШАГ 1)
├── architecture/
│   ├── hangmanUseCase.png           # Use Case диаграмма
│   ├── activity.png                 # Диаграмма активности
│   ├── class.png                    # Диаграмма классов
│   ├── *.mdj                        # Исходники диаграмм (StarUML)
│   └── REVIEW.md                    # Описание необходимых правок (ШАГ 2)
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
│           ├── game_window.py       # Игровой экран + кнопка подсказки (ШАГ 3)
│           ├── hint_dialog.py       # Диалог подсказки (choice/input/code) (ШАГ 4)
│           ├── main_menu.py         # Главное меню
│           ├── main_window.py       # Корневой виджет-стек
│           └── settings_window.py   # Настройки
├── educational/
│   ├── hint_system.py               # Класс QuestionBank (ШАГ 4)
│   └── questions.json               # 18 вопросов по Python (ШАГ 4)
└── tests/
    ├── test_hint_system.py          # Тесты QuestionBank (ШАГ 5)
    └── test_game_logic.py           # Тесты игровой логики (ШАГ 5)
```

---

## Ветки репозитория

| Ветка | Содержимое |
|---|---|
| `main` | Пустой корень проекта |
| `ba/game-description` | Аналитическая документация (папка `ba/`) |
| `feature/architecture` | Диаграммы UML (Use Case, Activity, Class) |
| `feature/programmists` | Игровой код + начальный вариант hint_system |
| `test/hint-system-validation` | Пустая ветка для тестировщика |
| `review/final` | **Финальная сборка** — содержит всё вышеперечисленное |

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
cd Hangman-on-the-Field-of-Miracles-main

# Запустить
python main.py
```

> **Важно:** запускать именно из папки `Hangman-on-the-Field-of-Miracles-main/`, иначе относительные пути к `assets/` не найдут нужные файлы.

### Запуск тестов

```bash
# Из корня репозитория hangman-project/
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
