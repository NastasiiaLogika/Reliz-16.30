from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
import sys
import math

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(400, 400, 350, 500)
        self.precision = 2  # Кількість знаків після коми за замовчуванням
        self.button_size = 80  # Початковий розмір кнопок
        self.mode = "calculator"  # Початковий режим: калькулятор
        self.UiComponents()
        self.show()

    def UiComponents(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Верхня панель для перемикання режимів
        self.mode_switch = QComboBox()
        self.mode_switch.addItems(["Калькулятор", "Рівняння", "Час", "Вага"])  # Додано новий пункт "Вага"
        self.mode_switch.currentIndexChanged.connect(self.change_mode)
        self.layout.addWidget(self.mode_switch)

        # Основна область для відображення інтерфейсу
        self.main_area = QStackedWidget()
        self.layout.addWidget(self.main_area)

        # Інтерфейс калькулятора
        self.calculator_widget = QWidget()
        self.calculator_layout = QVBoxLayout(self.calculator_widget)
        self.setup_calculator()
        self.main_area.addWidget(self.calculator_widget)

        # Інтерфейс для розв'язання рівнянь
        self.equation_widget = QWidget()
        self.equation_layout = QVBoxLayout(self.equation_widget)
        self.setup_equation_solver()
        self.main_area.addWidget(self.equation_widget)

        # Інтерфейс для перетворення часу
        self.time_widget = QWidget()
        self.time_layout = QVBoxLayout(self.time_widget)
        self.setup_time_converter()
        self.main_area.addWidget(self.time_widget)

        # Інтерфейс для перетворення ваги
        self.weight_widget = QWidget()
        self.weight_layout = QVBoxLayout(self.weight_widget)
        self.setup_weight_converter()
        self.main_area.addWidget(self.weight_widget)

        # Встановлюємо початковий режим
        self.main_area.setCurrentIndex(0)

    def setup_calculator(self):
        """Налаштування інтерфейсу калькулятора."""
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignRight)
        self.label.setFont(QFont('Arial', 20))
        self.label.setFixedHeight(60)
        self.label.setStyleSheet("border: 1px solid black;")
        self.calculator_layout.addWidget(self.label)

        grid_layout = QGridLayout()
        self.calculator_layout.addLayout(grid_layout)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('AC', 4, 0), ('del', 4, 1), ('cos', 4, 2), ('sin', 4, 3),
            ('tg', 5, 0), ('√', 5, 1), ('Precision', 5, 2), ('Zoom', 5, 3)
        ]

        self.button_map = {}
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFixedSize(self.button_size, self.button_size)
            button.setFont(QFont('Arial', 16))
            grid_layout.addWidget(button, row, col)
            self.button_map[text] = button

        self.button_map['='].setGraphicsEffect(QGraphicsColorizeEffect())

        self.button_map['+'].clicked.connect(self.action_plus)
        self.button_map['-'].clicked.connect(self.action_minus)
        self.button_map['/'].clicked.connect(self.action_div)
        self.button_map['*'].clicked.connect(self.action_mul)
        self.button_map['='].clicked.connect(self.action_equal)
        self.button_map['.'].clicked.connect(self.action_point)
        self.button_map['del'].clicked.connect(self.action_del)
        self.button_map['AC'].clicked.connect(self.action_clear)
        self.button_map['cos'].clicked.connect(self.action_cos)
        self.button_map['sin'].clicked.connect(self.action_sin)
        self.button_map['tg'].clicked.connect(self.action_tg)
        self.button_map['√'].clicked.connect(self.action_sqrt)
        self.button_map['Precision'].clicked.connect(self.change_precision)
        self.button_map['Zoom'].clicked.connect(self.change_button_size)

        for i in range(10):
            self.button_map[str(i)].clicked.connect(lambda checked, num=str(i): self.action_number(num))

    def setup_equation_solver(self):
        """Налаштування інтерфейсу для розв'язання рівнянь."""
        self.equation_label = QLabel("Введіть рівняння (наприклад, 2*x + 3 = 5):")
        self.equation_input = QLineEdit()
        self.equation_solve_button = QPushButton("Розв'язати")
        self.equation_result = QLabel("Результат: ")

        self.equation_layout.addWidget(self.equation_label)
        self.equation_layout.addWidget(self.equation_input)
        self.equation_layout.addWidget(self.equation_solve_button)
        self.equation_layout.addWidget(self.equation_result)

        self.equation_solve_button.clicked.connect(self.solve_equation)

    def setup_time_converter(self):
        """Налаштування інтерфейсу для перетворення часу."""
        self.time_label = QLabel("Введіть час:")
        self.time_input = QLineEdit()

        # Випадаючі списки для вибору одиниць вимірювання
        self.from_unit_time = QComboBox()
        self.from_unit_time.addItems(["Секунди", "Хвилини", "Години", "Дні", "Тижні", "Місяці", "Роки"])
        self.to_unit_time = QComboBox()
        self.to_unit_time.addItems(["Секунди", "Хвилини", "Години", "Дні", "Тижні", "Місяці", "Роки"])

        self.time_convert_button = QPushButton("Перетворити")
        self.time_result = QLabel("Результат: ")

        # Додаємо елементи до інтерфейсу
        self.time_layout.addWidget(self.time_label)
        self.time_layout.addWidget(self.time_input)
        self.time_layout.addWidget(QLabel("З:"))
        self.time_layout.addWidget(self.from_unit_time)
        self.time_layout.addWidget(QLabel("В:"))
        self.time_layout.addWidget(self.to_unit_time)
        self.time_layout.addWidget(self.time_convert_button)
        self.time_layout.addWidget(self.time_result)

        self.time_convert_button.clicked.connect(self.convert_time)

    def setup_weight_converter(self):
        """Налаштування інтерфейсу для перетворення ваги."""
        self.weight_label = QLabel("Введіть вагу:")
        self.weight_input = QLineEdit()

        # Випадаючі списки для вибору одиниць вимірювання
        self.from_unit_weight = QComboBox()
        self.from_unit_weight.addItems(["Кілограми", "Грами", "Міліграми", "Фунти", "Унції"])
        self.to_unit_weight = QComboBox()
        self.to_unit_weight.addItems(["Кілограми", "Грами", "Міліграми", "Фунти", "Унції"])

        self.weight_convert_button = QPushButton("Перетворити")
        self.weight_result = QLabel("Результат: ")

        # Додаємо елементи до інтерфейсу
        self.weight_layout.addWidget(self.weight_label)
        self.weight_layout.addWidget(self.weight_input)
        self.weight_layout.addWidget(QLabel("З:"))
        self.weight_layout.addWidget(self.from_unit_weight)
        self.weight_layout.addWidget(QLabel("В:"))
        self.weight_layout.addWidget(self.to_unit_weight)
        self.weight_layout.addWidget(self.weight_convert_button)
        self.weight_layout.addWidget(self.weight_result)

        self.weight_convert_button.clicked.connect(self.convert_weight)

    def change_mode(self, index):
        """Зміна режиму роботи."""
        self.main_area.setCurrentIndex(index)

    def action_equal(self):
        equation = self.label.text()
        try:
            ans = eval(equation)
            self.label.setText(str(round(ans, self.precision)))
        except:
            self.label.setText("Error")

    def action_plus(self):
        self.label.setText(self.label.text() + " + ")

    def action_minus(self):
        self.label.setText(self.label.text() + " - ")

    def action_div(self):
        self.label.setText(self.label.text() + " / ")

    def action_mul(self):
        self.label.setText(self.label.text() + " * ")

    def action_point(self):
        self.label.setText(self.label.text() + ".")

    def action_number(self, num):
        self.label.setText(self.label.text() + num)

    def action_clear(self):
        self.label.setText("")

    def action_del(self):
        text = self.label.text()
        self.label.setText(text[:-1])

    def action_cos(self):
        self.calculate_math_function(math.cos, "cos")

    def action_sin(self):
        self.calculate_math_function(math.sin, "sin")

    def action_tg(self):
        self.calculate_math_function(math.tan, "tg")

    def action_sqrt(self):
        self.calculate_math_function(math.sqrt, "√")

    def calculate_math_function(self, func, name):
        try:
            value = float(self.label.text())
            result = func(value)
            self.label.setText(f"{name}({value}) = {round(result, self.precision)}")
        except ValueError:
            self.label.setText("Error")

    def change_precision(self):
        precision, ok = QInputDialog.getInt(self, "Precision", "Введіть кількість знаків після коми:", self.precision, 0, 10)
        if ok:
            self.precision = precision
            self.label.setText(f"Precision set to {self.precision}")

    def change_button_size(self):
        size, ok = QInputDialog.getInt(self, "Zoom", "Введіть розмір кнопок (в пікселях):", self.button_size, 50, 150)
        if ok:
            self.button_size = size
            self.update_button_sizes()

    def update_button_sizes(self):
        for button in self.button_map.values():
            button.setFixedSize(self.button_size, self.button_size)

    def solve_equation(self):
        """Розв'язання рівняння."""
        equation = self.equation_input.text()
        try:
            from sympy import symbols, Eq, solve
            x = symbols('x')
            eq = Eq(eval(equation.split('=')[0]), eval(equation.split('=')[1]))
            solution = solve(eq, x)
            self.equation_result.setText(f"Результат: {solution}")
        except Exception as e:
            self.equation_result.setText(f"Помилка: {e}")

    def convert_time(self):
        """Перетворення часу між одиницями."""
        try:
            time_value = float(self.time_input.text())
            from_unit = self.from_unit_time.currentText()
            to_unit = self.to_unit_time.currentText()

            # Конвертація в секунди
            if from_unit == "Секунди":
                seconds = time_value
            elif from_unit == "Хвилини":
                seconds = time_value * 60
            elif from_unit == "Години":
                seconds = time_value * 3600
            elif from_unit == "Дні":
                seconds = time_value * 86400
            elif from_unit == "Тижні":
                seconds = time_value * 604800
            elif from_unit == "Місяці":
                seconds = time_value * 2629800  # Середньостатистичний місяць
            elif from_unit == "Роки":
                seconds = time_value * 31557600  # Середньостатистичний рік

            # Конвертація з секунд у вибрану одиницю
            if to_unit == "Секунди":
                result = seconds
            elif to_unit == "Хвилини":
                result = seconds / 60
            elif to_unit == "Години":
                result = seconds / 3600
            elif to_unit == "Дні":
                result = seconds / 86400
            elif to_unit == "Тижні":
                result = seconds / 604800
            elif to_unit == "Місяці":
                result = seconds / 2629800
            elif to_unit == "Роки":
                result = seconds / 31557600

            self.time_result.setText(f"Результат: {round(result, self.precision)} {to_unit.lower()}")
        except ValueError:
            self.time_result.setText("Помилка: введіть число")

    def convert_weight(self):
        """Перетворення ваги між одиницями."""
        try:
            weight_value = float(self.weight_input.text())
            from_unit = self.from_unit_weight.currentText()
            to_unit = self.to_unit_weight.currentText()

            # Конвертація в кілограми
            if from_unit == "Кілограми":
                kilograms = weight_value
            elif from_unit == "Грами":
                kilograms = weight_value / 1000
            elif from_unit == "Міліграми":
                kilograms = weight_value / 1_000_000
            elif from_unit == "Фунти":
                kilograms = weight_value * 0.453592
            elif from_unit == "Унції":
                kilograms = weight_value * 0.0283495

            # Конвертація з кілограмів у вибрану одиницю
            if to_unit == "Кілограми":
                result = kilograms
            elif to_unit == "Грами":
                result = kilograms * 1000
            elif to_unit == "Міліграми":
                result = kilograms * 1_000_000
            elif to_unit == "Фунти":
                result = kilograms / 0.453592
            elif to_unit == "Унції":
                result = kilograms / 0.0283495

            self.weight_result.setText(f"Результат: {round(result, self.precision)} {to_unit.lower()}")
        except ValueError:
            self.weight_result.setText("Помилка: введіть число")

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec())