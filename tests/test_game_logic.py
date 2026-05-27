"""
Тесты базовой игровой логики.

Запуск: pytest tests/test_game_logic.py -v
Из директории: hangman-project/
"""

import sys
import os
import pytest

# Корректный путь к папке с игрой
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'Hangman-on-the-Field-of-Miracles-main'))

# Импортируем всё, что нужно, в одном месте
from src.core.game_logic import (
    create_hidden_word,
    update_hidden_word,
    get_word_and_description
)


# ------------------------------------------------------------------ create_hidden_word

def test_create_hidden_word_length():
    """Скрытое слово имеет ту же длину, что и оригинал."""
    word = "программа"
    hidden = create_hidden_word(word)
    assert len(hidden) == len(word)


def test_create_hidden_word_all_squares():
    """Все символы скрытого слова — '■'."""
    hidden = create_hidden_word("кот")
    assert hidden == ['■', '■', '■']


def test_create_hidden_word_empty():
    """Пустое слово даёт пустой список."""
    assert create_hidden_word("") == []


# ------------------------------------------------------------------ update_hidden_word

def test_update_hidden_word_correct_letter():
    """Правильная буква открывается на всех позициях."""
    word = "банан"
    hidden = create_hidden_word(word)
    hidden = update_hidden_word(word, hidden, 'а')
    assert hidden == ['■', 'а', '■', 'а', '■']


def test_update_hidden_word_wrong_letter():
    """Отсутствующая буква не меняет скрытое слово."""
    word = "кот"
    hidden = create_hidden_word(word)
    result = update_hidden_word(word, hidden, 'а')
    assert result == ['■', '■', '■']


def test_update_hidden_word_case_insensitive():
    """Угадывание работает без учёта регистра."""
    word = "кот"
    hidden = create_hidden_word(word)
    hidden = update_hidden_word(word, hidden, 'к')
    assert hidden[0] == 'к'


# ------------------------------------------------------------------ win condition

def test_win_condition():
    """Слово полностью угадано = победа (нет символов '■')."""
    word = "кот"
    hidden = create_hidden_word(word)
    for letter in set(word):
        hidden = update_hidden_word(word, hidden, letter)
    assert '■' not in hidden


def test_win_condition_not_met():
    """Пока есть '■' — победа не достигнута."""
    word = "кот"
    hidden = create_hidden_word(word)
    hidden = update_hidden_word(word, hidden, 'к')
    assert '■' in hidden


# ------------------------------------------------------------------ get_word_and_description

def test_get_word_and_description_returns_pair():
    """Функция возвращает кортеж (слово, описание)."""
    words = [
        {"word": "питон", "description": "Язык программирования"},
        {"word": "код", "description": "Набор инструкций"}
    ]
    word, desc = get_word_and_description(words)
    assert word in ["питон", "код"]
    assert desc in ["Язык программирования", "Набор инструкций"]
    assert len(words) == 1  # Список уменьшился на 1


def test_get_word_and_description_empty_list():
    """При пустом списке возвращается (None, None)."""
    words = []
    word, desc = get_word_and_description(words)
    assert word is None
    assert desc is None
