
import sys
from googletrans import Translator, LANGUAGES
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QHBoxLayout, QTextEdit, QComboBox,
    QPushButton
)

class SimpleTranslator(QWidget):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Simple Translator')
        self.setGeometry(200, 200, 600, 300)

        # Віджети
        self.input = QTextEdit()
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        
        self.lang_from = QComboBox()
        self.lang_to = QComboBox()
        for code, name in LANGUAGES.items():
            self.lang_from.addItem(name.title(), code)
            self.lang_to.addItem(name.title(), code)
        self.lang_to.setCurrentText('Ukrainian')
        
        self.btn_translate = QPushButton('Перекласти')
        self.btn_translate.clicked.connect(self.do_translate)

        # Розмітка
        layout = QVBoxLayout()
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(self.lang_from)
        lang_layout.addWidget(self.lang_to)
        
        layout.addLayout(lang_layout)
        layout.addWidget(self.input)
        layout.addWidget(self.btn_translate)
        layout.addWidget(self.output)
        
        self.setLayout(layout)

    def do_translate(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
            
        try:
            src = self.lang_from.currentData()
            dest = self.lang_to.currentData()
            result = self.translator.translate(text, src=src, dest=dest)
            self.output.setPlainText(result.text)
        except Exception as e:
            self.output.setPlainText(f"Помилка: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trans = SimpleTranslator()
    trans.show()
    sys.exit(app.exec_())
