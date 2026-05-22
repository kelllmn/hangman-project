# educational_hint.py
import json
import random

class EducationalHint:
    """Система обучающих подсказок по дисциплине 'Основы и методологии программирования'"""
    
    def __init__(self, questions_file='educational_questions.json'):
        with open(questions_file, 'r', encoding='utf-8') as f:
            self.questions = json.load(f)
    
    def get_random_question(self):
        """Выбирает случайный вопрос"""
        return random.choice(self.questions)
    
    def show_hint(self):
        """Показывает вопрос с вариантами ответов и возвращает подсказку"""
        question = self.get_random_question()
        
        print("\n" + "="*60)
        print("🎓 ОБУЧАЮЩИЙ ЭЛЕМЕНТ - Основы и методологии программирования 🎓")
        print("="*60)
        print(f"\n❓ {question['question']}\n")
        
        # Показываем варианты ответов
        for i, option in enumerate(question['options'], 1):
            print(f"   {i}. {option}")
        
        # Получаем ответ
        print("\n👉 Введите номер правильного ответа: ", end="")
        answer = input()
        
        # Проверяем ответ
        try:
            choice = int(answer) - 1
            if 0 <= choice < len(question['options']):
                if question['options'][choice] == question['correct']:
                    print(f"\n✅ Правильно! Вы получаете подсказку: {question['hint']}")
                    return question['hint']
                else:
                    print(f"\n❌ Неправильно! Правильный ответ: {question['correct']}")
                    return None
            else:
                print("\n❌ Неверный номер варианта!")
                return None
        except ValueError:
            print("\n❌ Введите число!")
            return None

# Функция для тестирования (можно удалить потом)
if __name__ == "__main__":
    hint_system = EducationalHint()
    hint_system.show_hint()
