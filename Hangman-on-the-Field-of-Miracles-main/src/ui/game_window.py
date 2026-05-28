import random
import sys
import os

from PyQt6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout, QWidget,
    QGridLayout, QTextEdit, QMessageBox, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from src.core.game_logic import get_word_and_description, create_hidden_word, update_hidden_word

# Добавляем корень проекта в sys.path, чтобы найти папку educational
_project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..')
)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from educational.hint_system import QuestionBank
from src.ui.hint_dialog import HintDialog

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class HangmanGame(QWidget):
    def __init__(self, parent=None, words=None, hangman_stages=None):
        super().__init__(parent)
        self.words = words
        self.hangman_stages = hangman_stages
        # Банк вопросов живёт весь сеанс — вопросы не повторяются между раундами
        self.question_bank = QuestionBank()
        self.initUI()
        self.start_new_game()

    def initUI(self):
        layout = QVBoxLayout()

        self.hangman_text = QTextEdit(self)
        self.hangman_text.setReadOnly(True)
        self.hangman_text.setFont(QFont('Courier', 18))
        self.hangman_text.setStyleSheet("")  # цвета из styles.css
        layout.addWidget(self.hangman_text)

        self.word_label = QLabel(" ", self)
        self.word_label.setFont(QFont('Arial', 20))
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.word_label)

        self.description_label = QLabel("", self)
        self.description_label.setFont(QFont('Arial', 16))
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.description_label)

        self.buttons_layout = QGridLayout()
        layout.addLayout(self.buttons_layout)
        self.create_alphabet_buttons()

        # Кнопка подсказки
        self.hint_button = QPushButton("💡 Подсказка", self)
        self.hint_button.setFont(QFont('Arial', 14))
        self.hint_button.clicked.connect(self.on_hint_clicked)
        layout.addWidget(self.hint_button)

        self.new_game_button = QPushButton("Новая игра", self)
        self.new_game_button.setFont(QFont('Arial', 14))
        self.new_game_button.clicked.connect(self.start_new_game)
        layout.addWidget(self.new_game_button)

        self.back_to_menu_button = QPushButton("Главное меню", self)
        self.back_to_menu_button.setFont(QFont('Arial', 14))
        self.back_to_menu_button.clicked.connect(self.back_to_menu)
        layout.addWidget(self.back_to_menu_button)

        self.setLayout(layout)

    def create_alphabet_buttons(self):
        for index, letter in enumerate(ALPHABET):
            button = QPushButton(letter.upper(), self)
            button.setFont(QFont('Arial', 14))
            button.setFixedSize(40, 40)
            button.clicked.connect(self.handle_letter_click)
            self.buttons_layout.addWidget(button, index // 8, index % 8)

    def get_hangman_stage(self, stage):
        return self.hangman_stages[stage] if 0 <= stage < len(self.hangman_stages) else "Ошибка загрузки изображения"

    def start_new_game(self):
        self.lives = len(self.hangman_stages) - 1
        self.stage = 0
        self.word, self.description = get_word_and_description(self.words)
        self.hidden_word = create_hidden_word(self.word)
        # Сбрасываем состояние подсказки для нового раунда
        self.hint_used = False
        self.hint_button.setEnabled(True)
        self._enable_all_letter_buttons()
        self.update_ui()

    def update_ui(self):
        self.word_label.setText(" ".join(self.hidden_word))
        self.description_label.setText(self.description)
        self.hangman_text.setText(self.get_hangman_stage(self.stage))
        # Кнопка подсказки неактивна, если все буквы уже открыты
        if '■' not in self.hidden_word:
            self.hint_button.setEnabled(False)

    def handle_letter_click(self):
        sender = self.sender()
        letter = sender.text().lower()
        # Блокируем кнопку сразу после нажатия
        sender.setEnabled(False)
        if letter in self.word:
            self.hidden_word = update_hidden_word(self.word, self.hidden_word, letter)
            self.update_ui()
            if '■' not in self.hidden_word:
                self.hint_button.setEnabled(False)
                self.show_message("Поздравляю, ты выиграл!", QMessageBox.Icon.Information)
        else:
            self.lives -= 1
            self.stage += 1
            if self.lives == 0:
                self.stage = len(self.hangman_stages) - 1
                self.update_ui()
                self.show_message(f"Игра окончена! Слово было: {self.word}", QMessageBox.Icon.Critical)
            else:
                self.update_ui()

    def on_hint_clicked(self):
        """Открывает диалог с вопросом и обрабатывает результат."""
        if self.hint_used:
            return
        question = self.question_bank.get_random_question()
        dialog = HintDialog(question, parent=self)
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted and dialog.answered_correctly:
            # Правильный ответ — открываем случайную букву
            self.reveal_random_letter()
            self.hint_used = True
            self.hint_button.setEnabled(False)
        elif dialog.submitted and not dialog.answered_correctly:
            # Неправильный ответ — блокируем кнопку без открытия буквы
            self.hint_used = True
            self.hint_button.setEnabled(False)
        # Иначе пользователь закрыл без ответа — кнопка остаётся активной

    def reveal_random_letter(self):
        """Открывает одну случайную ещё не угаданную букву в слове."""
        hidden_positions = [i for i, ch in enumerate(self.hidden_word) if ch == '■']
        if not hidden_positions:
            return
        pos = random.choice(hidden_positions)
        letter = self.word[pos]
        self.hidden_word = update_hidden_word(self.word, self.hidden_word, letter)
        self.update_ui()
        # Проверяем победу после открытия буквы
        if '■' not in self.hidden_word:
            self.hint_button.setEnabled(False)
            self.show_message("Поздравляю, ты выиграл!", QMessageBox.Icon.Information)

    def show_message(self, text, icon):
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle("Результат")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.buttonClicked.connect(self.handle_message_button_click)
        msg_box.exec()

    def handle_message_button_click(self, button):
        if self.sender().text() == "OK":
            self.start_new_game()

    def back_to_menu(self):
        self.parentWidget().setCurrentIndex(0)

    def _enable_all_letter_buttons(self):
        """Разблокирует все кнопки алфавита для нового раунда."""
        for i in range(self.buttons_layout.count()):
            widget = self.buttons_layout.itemAt(i).widget()
            if widget:
                widget.setEnabled(True)
