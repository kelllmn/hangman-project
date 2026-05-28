import json
import random
import os


class QuestionBank:
    """Банк обучающих вопросов по Python для системы подсказок."""

    def __init__(self, questions_file='questions.json'):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, questions_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)
        self.used_ids: set = set()

    def get_random_question(self) -> dict:
        """Возвращает случайный неиспользованный вопрос.

        Если все вопросы сессии исчерпаны — сбрасывает список и начинает новый цикл.
        """
        available = [q for q in self.questions if q['id'] not in self.used_ids]
        if not available:
            self.reset_session()
            available = self.questions[:]
        question = random.choice(available)
        self.mark_used(question['id'])
        return question

    def mark_used(self, question_id: int) -> None:
        """Помечает вопрос как использованный в текущей сессии."""
        self.used_ids.add(question_id)

    def reset_session(self) -> None:
        """Сбрасывает список использованных вопросов (начало новой сессии)."""
        self.used_ids.clear()

    def check_answer(self, question: dict, user_answer: str) -> bool:
        """Проверяет ответ пользователя без учёта регистра и пробелов по краям."""
        return user_answer.strip().lower() == str(question['correct']).strip().lower()
