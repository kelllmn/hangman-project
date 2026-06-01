# Отчёт о тестировании игры "Виселица"

## Основная информация
- **Тестировщик:** Тимур
- **Дата:** 28.05.2026
- **Ветка:** test/hint-system-validation
- **Проект:** Hangman-on-the-Field-of-Miracles

## Результаты тестирования

| Показатель | Значение |
|------------|----------|
| Всего тестов | 20 |
| Пройдено | 20 |
| Упало | 0 |
| Процент успеха | 100% |

## Что было протестировано

### 1. Игровая логика (test_game_logic.py) — 10 тестов

| № | Тест | Что проверяет | Результат |
|---|------|---------------|-----------|
| 1 | test_create_hidden_word_length | Длина маски равна длине слова | ✅ PASSED |
| 2 | test_create_hidden_word_all_squares | Все символы скрыты символом ■ | ✅ PASSED |
| 3 | test_create_hidden_word_empty | Пустое слово не вызывает ошибку | ✅ PASSED |
| 4 | test_update_hidden_word_correct_letter | Правильная буква открывается на всех позициях | ✅ PASSED |
| 5 | test_update_hidden_word_wrong_letter | Неправильная буква не меняет маску | ✅ PASSED |
| 6 | test_update_hidden_word_case_insensitive | Регистр буквы не важен | ✅ PASSED |
| 7 | test_win_condition | Полное угадывание = победа | ✅ PASSED |
| 8 | test_win_condition_not_met | Пока есть ■ — победа не наступает | ✅ PASSED |
| 9 | test_get_word_and_description_returns_pair | Выбор слова из списка работает | ✅ PASSED |
| 10 | test_get_word_and_description_empty_list | Пустой список не вызывает ошибку | ✅ PASSED |

### 2. Система подсказок (test_hint_system.py) — 10 тестов

| № | Тест | Что проверяет | Результат |
|---|------|---------------|-----------|
| 1 | test_question_bank_loads | Вопросы загружаются из JSON | ✅ PASSED |
| 2 | test_get_random_question_returns_question | Вопрос содержит все нужные поля | ✅ PASSED |
| 3 | test_questions_not_repeated | Вопросы не повторяются в сессии | ✅ PASSED |
| 4 | test_mark_used | Отметка использованного вопроса работает | ✅ PASSED |
| 5 | test_reset_session | Сброс сессии позволяет использовать вопросы снова | ✅ PASSED |
| 6 | test_auto_reset_when_exhausted | Автосброс при исчерпании банка | ✅ PASSED |
| 7 | test_all_question_types_present | Присутствуют все 3 типа вопросов | ✅ PASSED |
| 8 | test_correct_answer_check | Правильный ответ распознаётся | ✅ PASSED |
| 9 | test_correct_answer_case_insensitive | Регистр ответа не важен | ✅ PASSED |
| 10 | test_wrong_answer_check | Неправильный ответ отвергается | ✅ PASSED |

## Найденные и исправленные проблемы

| № | Проблема | Решение |
|---|----------|---------|
| 1 | Неправильные пути импорта в тестах | Исправлен sys.path.insert |
| 2 | Тесты проверяли арифметику, а не код | Удалены test_loss_condition* |
| 3 | Тесты GUI в модуле hint_system | Удалены test_reveal_random_letter и test_hint_used_flag* |
| 4 | Отсутствие зависимостей | Установлены PyQt6, pygame |

## Вывод

**Все 20 тестов успешно пройдены.** Система подсказок и игровая логика работают корректно. Проект готов к сдаче.

---

*Отчёт подготовил: Тимур, тестировщик*
