from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class HintDialog(QDialog):
    """Диалоговое окно обучающей подсказки.

    Поддерживает три типа вопросов:
      - choice : выбор из 4 вариантов
      - input  : ввод ответа вручную
      - code   : дополнение фрагмента кода
    """

    def __init__(self, question: dict, parent=None):
        super().__init__(parent)
        self.question = question
        self.answered_correctly = False
        # True если пользователь отправил ответ (верный или нет), False если просто закрыл
        self.submitted = False
        self.setWindowTitle("💡 Обучающая подсказка")
        self.setMinimumWidth(480)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(12)

        header = QLabel("🎓 Ответьте на вопрос по Python, чтобы получить подсказку")
        header.setFont(QFont('Arial', 12))
        header.setWordWrap(True)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)

        q_label = QLabel(self.question['question'])
        q_label.setFont(QFont('Arial', 13))
        q_label.setWordWrap(True)
        layout.addWidget(q_label)

        q_type = self.question.get('type', 'input')
        if q_type == 'choice':
            self._add_choice_area(layout)
        elif q_type == 'code':
            self._add_code_area(layout)
        else:
            self._add_input_area(layout)

        back_btn = QPushButton("Вернуться к игре")
        back_btn.setFont(QFont('Arial', 12))
        back_btn.clicked.connect(self.reject)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    # ------------------------------------------------------------------ choice

    def _add_choice_area(self, layout: QVBoxLayout):
        for option in self.question.get('options', []):
            btn = QPushButton(option)
            btn.setFont(QFont('Arial', 12))
            btn.setFixedHeight(36)
            btn.clicked.connect(self._on_choice_clicked)
            layout.addWidget(btn)

    def _on_choice_clicked(self):
        self._evaluate(self.sender().text())

    # ------------------------------------------------------------------ input

    def _add_input_area(self, layout: QVBoxLayout):
        self.answer_edit = QLineEdit()
        self.answer_edit.setFont(QFont('Arial', 13))
        self.answer_edit.setPlaceholderText("Введите ответ...")
        self.answer_edit.returnPressed.connect(self._on_submit)
        layout.addWidget(self.answer_edit)

        submit_btn = QPushButton("Ответить")
        submit_btn.setFont(QFont('Arial', 12))
        submit_btn.clicked.connect(self._on_submit)
        layout.addWidget(submit_btn)

    def _on_submit(self):
        self._evaluate(self.answer_edit.text())

    # ------------------------------------------------------------------ code

    def _add_code_area(self, layout: QVBoxLayout):
        code_text = self.question.get('hint_for_code', '')
        code_label = QLabel(code_text)
        code_label.setFont(QFont('Courier New', 12))
        code_label.setStyleSheet(
            "background-color: #181825; border: 1px solid #45475a; padding: 8px; color: #a6e3a1;"
        )
        code_label.setWordWrap(True)
        layout.addWidget(code_label)

        fill_label = QLabel("Введите пропущенное слово/выражение (вместо ___):")
        fill_label.setFont(QFont('Arial', 11))
        layout.addWidget(fill_label)

        self.answer_edit = QLineEdit()
        self.answer_edit.setFont(QFont('Courier New', 13))
        self.answer_edit.setPlaceholderText("___")
        self.answer_edit.returnPressed.connect(self._on_submit)
        layout.addWidget(self.answer_edit)

        submit_btn = QPushButton("Ответить")
        submit_btn.setFont(QFont('Arial', 12))
        submit_btn.clicked.connect(self._on_submit)
        layout.addWidget(submit_btn)

    # ------------------------------------------------------------------ logic

    def _evaluate(self, user_answer: str):
        self.submitted = True
        correct = str(self.question['correct']).strip().lower()
        if user_answer.strip().lower() == correct:
            self.answered_correctly = True
            self.accept()
        else:
            QMessageBox.warning(
                self,
                "Неверно",
                f"Неправильный ответ.\nПравильно: {self.question['correct']}"
            )
            self.answered_correctly = False
            self.reject()
