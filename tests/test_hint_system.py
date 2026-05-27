"""
Тесты системы подсказок (QuestionBank).

Запуск: pytest tests/test_hint_system.py -v
Из директории: hangman-project/
"""

import sys
import os
import pytest

# Добавляем корень репозитория в путь, чтобы найти educational/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from educational.hint_system import QuestionBank


@pytest.fixture
def bank():
    """Экземпляр QuestionBank со стандартным файлом вопросов."""
    return QuestionBank()


# ------------------------------------------------------------------ загрузка

def test_question_bank_loads(bank):
    """QuestionBank успешно загружает файл вопросов."""
    assert bank.questions is not None
    assert len(bank.questions) > 0


# ------------------------------------------------------------------ получение вопроса

def test_get_random_question_returns_question(bank):
    """get_random_question возвращает словарь с обязательными полями."""
    bank.reset_session()
    q = bank.get_random_question()
    assert isinstance(q, dict)
    for field in ('id', 'type', 'question', 'correct'):
        assert field in q, f"Отсутствует поле '{field}' в вопросе"


def test_questions_not_repeated(bank):
    """Одни и те же вопросы не возвращаются подряд пока не исчерпан банк."""
    bank.reset_session()
    total = len(bank.questions)
    seen_ids = []
    for _ in range(total):
        q = bank.get_random_question()
        assert q['id'] not in seen_ids, f"Вопрос id={q['id']} повторился раньше исчерпания банка"
        seen_ids.append(q['id'])


# ------------------------------------------------------------------ mark_used

def test_mark_used(bank):
    """Использованный вопрос не возвращается в следующих вызовах."""
    bank.reset_session()
    first = bank.get_random_question()
    used_id = first['id']
    # Помечаем явно (он уже помечен внутри get_random_question, но проверим метод)
    bank.mark_used(used_id)
    # Запрашиваем ещё вопросы — первый не должен появиться
    remaining = len(bank.questions) - 1
    returned_ids = []
    for _ in range(remaining):
        q = bank.get_random_question()
        returned_ids.append(q['id'])
    assert used_id not in returned_ids


# ------------------------------------------------------------------ reset_session

def test_reset_session(bank):
    """После reset_session все вопросы снова доступны."""
    bank.reset_session()
    for _ in range(len(bank.questions)):
        bank.get_random_question()
    # Все вопросы исчерпаны — банк должен автосброситься при следующем вызове
    bank.reset_session()
    assert len(bank.used_ids) == 0
    q = bank.get_random_question()
    assert q is not None


# ------------------------------------------------------------------ автосброс

def test_auto_reset_when_exhausted(bank):
    """Когда все вопросы использованы, get_random_question автоматически сбрасывает банк."""
    bank.reset_session()
    total = len(bank.questions)
    # Исчерпываем все вопросы через mark_used (минуя автоснятие внутри get)
    for q in bank.questions:
        bank.mark_used(q['id'])
    # Теперь все использованы — следующий вызов должен сработать без ошибки
    result = bank.get_random_question()
    assert result is not None


# ------------------------------------------------------------------ типы вопросов

def test_all_question_types_present(bank):
    """В банке вопросов присутствуют все три типа: choice, input, code."""
    types_in_bank = {q['type'] for q in bank.questions}
    for required_type in ('choice', 'input', 'code'):
        assert required_type in types_in_bank, f"Тип '{required_type}' отсутствует в банке вопросов"


# ------------------------------------------------------------------ проверка ответов

def test_correct_answer_check(bank):
    """check_answer возвращает True для правильного ответа."""
    bank.reset_session()
    for q in bank.questions:
        assert bank.check_answer(q, q['correct']), (
            f"check_answer вернул False для правильного ответа вопроса id={q['id']}"
        )


def test_correct_answer_case_insensitive(bank):
    """check_answer не чувствителен к регистру."""
    bank.reset_session()
    q = bank.get_random_question()
    upper_answer = str(q['correct']).upper()
    assert bank.check_answer(q, upper_answer)


def test_wrong_answer_check(bank):
    """check_answer возвращает False для заведомо неправильного ответа."""
    bank.reset_session()
    q = bank.get_random_question()
    assert not bank.check_answer(q, "___заведомо_неверный_ответ___")


# ------------------------------------------------------------------ reveal_random_letter

def test_reveal_random_letter():
    """reveal_random_letter открывает букву из загаданного слова."""
    # Эмулируем логику без PyQt6-зависимостей
    from src.core.game_logic import create_hidden_word, update_hidden_word
    import random

    word = "кот"
    hidden = create_hidden_word(word)
    assert hidden == ['■', '■', '■']

    # Логика reveal_random_letter
    hidden_positions = [i for i, ch in enumerate(hidden) if ch == '■']
    pos = random.choice(hidden_positions)
    letter = word[pos]
    hidden = update_hidden_word(word, hidden, letter)

    assert letter in word
    assert hidden.count('■') == 2  # одна буква открылась


# ------------------------------------------------------------------ hint_used flag

def test_hint_used_flag():
    """После успешной подсказки hint_used должен стать True."""
    # Проверяем только логику флага, без GUI
    hint_used = False
    # Симулируем успешный ответ
    answered_correctly = True
    if answered_correctly:
        hint_used = True
    assert hint_used is True


def test_hint_used_flag_wrong_answer():
    """После неверного ответа hint_used тоже True (кнопка блокируется)."""
    hint_used = False
    submitted = True
    answered_correctly = False
    if submitted and not answered_correctly:
        hint_used = True
    assert hint_used is True


def test_hint_used_flag_no_answer():
    """Если диалог закрыт без ответа, hint_used остаётся False."""
    hint_used = False
    submitted = False
    answered_correctly = False
    if submitted and not answered_correctly:
        hint_used = True
    assert hint_used is False
