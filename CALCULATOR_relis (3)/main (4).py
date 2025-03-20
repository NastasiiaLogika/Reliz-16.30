from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
from PyQt5 import*
import sys
import math

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calaulator")
        self.setGeometry(400, 400, 530, 350 )
        self.UiComponents()
        self.show()


    def UiComponents(self):
        self.label = QLabel(self)
        self.label.setGeometry(5, 5, 520, 70)
        self.label.setWordWrap(True)
        
        self.label.setAlignment(Qt.AlignRight)
        self.label.setFont(QFont('Arial', 15))

        push1 = QPushButton("1",self)
        push1.setGeometry(5, 150, 80, 40)

        push2 = QPushButton("2",self)
        push2.setGeometry(95, 150, 80, 40)

        push3 = QPushButton("3",self)
        push3.setGeometry(185, 150, 80, 40)

        push4 = QPushButton("4",self)
        push4.setGeometry(5, 200, 80, 40)

        push5 = QPushButton("5",self)
        push5.setGeometry(95, 200, 80, 40)

        push6 = QPushButton("6",self)
        push6.setGeometry(185, 200, 80, 40)

        push7 = QPushButton("7",self)
        push7.setGeometry(5, 250, 80, 40)

        push8 = QPushButton("8",self)
        push8.setGeometry(95, 250, 80, 40)

        push9 = QPushButton("9",self)
        push9.setGeometry(185, 250, 80, 40)

        push0 = QPushButton("0",self)
        push0.setGeometry(5, 300, 80, 40)

        push_dot = QPushButton(".",self)
        push_dot.setGeometry(95, 300, 80, 40)

        push_div = QPushButton("/",self)
        push_div.setGeometry(185, 300, 80, 40)

        push_plus = QPushButton("+",self)
        push_plus.setGeometry(275, 150, 80, 40)

        push_cos = QPushButton("cos",self)
        push_cos.setGeometry(365, 150, 80, 40)

        push_sin = QPushButton("sin",self)
        push_sin.setGeometry(365, 200, 80, 40)

        push_tg = QPushButton("tg",self)
        push_tg.setGeometry(365, 250, 80, 40)

        push_sqrt= QPushButton("√",self)
        push_sqrt.setGeometry(275, 300, 80, 40)
        
        push_minus = QPushButton("-",self)
        push_minus.setGeometry(275, 200, 80, 40)

        push_mul = QPushButton("*",self)
        push_mul.setGeometry(275, 250, 80, 40)

        push_equal = QPushButton("=",self)
        push_equal.setGeometry(450, 100, 80, 40)

        push_clear = QPushButton("AC",self)
        push_clear.setGeometry(5, 100, 215, 40)

        push_del = QPushButton("del",self)
        push_del.setGeometry(230, 100, 215, 40)

        push_pow = QPushButton("pow",self)
        push_pow.setGeometry(450, 150, 80, 40)

        push_bracket1 = QPushButton("(",self)
        push_bracket1.setGeometry(450, 200, 80, 40)

        push_bracket2 = QPushButton(")",self)
        push_bracket2.setGeometry(450, 250, 80, 40)

        push_ln = QPushButton("ln",self)
        push_ln.setGeometry(450, 300, 80, 40)

        push_log = QPushButton("log",self)
        push_log.setGeometry(365, 300, 80, 40)
        


        c_effect = QGraphicsColorizeEffect()
        c_effect.setColor(Qt.blue)
        push_equal.setGraphicsEffect(c_effect)


        push_minus.clicked.connect(self.action_minus)
        push_div.clicked.connect(self.action_div)
        push_equal.clicked.connect(self.action_equal)
        push_mul.clicked.connect(self.action_mul)
        push_plus.clicked.connect(self.action_plus)

        push_dot.clicked.connect(self.action_point)
        push_del.clicked.connect(self.action_del)
        push_clear.clicked.connect(self.action_clear)

        push0.clicked.connect(self.action0)
        push1.clicked.connect(self.action1)
        push2.clicked.connect(self.action2)
        push3.clicked.connect(self.action3)
        push4.clicked.connect(self.action4)
        push5.clicked.connect(self.action5)
        push6.clicked.connect(self.action6)
        push7.clicked.connect(self.action7)
        push8.clicked.connect(self.action8)
        push9.clicked.connect(self.action9)

        push_cos.clicked.connect(self.action_cos)
        push_sin.clicked.connect(self.action_sin)
        push_tg.clicked.connect(self.action_tg)
        push_sqrt.clicked.connect(self.action_sqrt)
        push_pow.clicked.connect(self.action_pow)
        push_bracket1.clicked.connect(self.bracket_front)
        push_bracket2.clicked.connect(self.action_end)
        push_ln.clicked.connect(self.action_ln)
        push_log.clicked.connect(self.action_log)





    def action_equal(self):
        equation = self.label.text()
        try:
            ans =eval(equation)
            self.label.setText(str(ans))
        except:
            self.label.setText("неправельний ввід")

    def action_plus(self):
        text = self.label.text()
        self.label.setText(text + " + ")

########################################
    def bracket_front(self):
        text = self.label.text()
        self.label.setText(text + " ( ")

    def action_end(self):
        text = self.label.text()
        self.label.setText(text + " ) ")
########################################
    def action_minus(self):
        text = self.label.text()
        self.label.setText(text + " - ")

    def action_div(self):
        text = self.label.text()
        self.label.setText(text + " / ")

    def action_mul(self):
        text = self.label.text()
        self.label.setText(text + " * ")

    def action_point(self):
        text = self.label.text()
        self.label.setText(text + ".")

    def action0(self):
        text = self.label.text()
        self.label.setText(text + "0")

    def action1(self):
        text = self.label.text()
        self.label.setText(text + "1")
    
    def action2(self):
        text = self.label.text()
        self.label.setText(text + "2")

    def action3(self):
        text = self.label.text()
        self.label.setText(text + "3")

    def action4(self):
        text = self.label.text()
        self.label.setText(text + "4")
    
    def action5(self):
        text = self.label.text()
        self.label.setText(text + "5")

    def action6(self):
        text = self.label.text()
        self.label.setText(text + "6")

    def action7(self):
        text = self.label.text()
        self.label.setText(text + "7")
    
    def action8(self):
        text = self.label.text()
        self.label.setText(text + "8")

    def action9(self):
        text = self.label.text()
        self.label.setText(text + "9")

    def action_clear(self):
        self.label.setText("")

    def action_del(self):
        text = self.label.text()
        print(text[:len(text)-1])
        self.label.setText(text[:len(text)-1])

    def action_cos(self):
        text = self.label.text()
        
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.cos(value)
            self.label.setText(f"cos({text}) = {result}")
        except ValueError:
            # Якщо текст не можна перетворити в число
            self.label.setText("Invalid input")

    def action_sin(self):
        text = self.label.text()
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.sin(value)
            self.label.setText(f"sin({text}) = {result}")
        except ValueError:
            # Якщо текст не можна перетворити в число
            self.label.setText("Invalid input")
        

    def action_tg(self):
        text = self.label.text()
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.tan(value)
            self.label.setText(f"tg({text}) = {result}")
        except ValueError:
            # Якщо текст не можна перетворити в число
            self.label.setText("Invalid input")

    def action_sqrt(self):
        text = self.label.text()
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.sqrt(value)
            self.label.setText(f"√({text}) = {result}")
        except ValueError:
            # Якщо текст не можна перетворити в число
            self.label.setText("Invalid input")

    def action_pow(self):
        text = self.label.text()
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.pow(value, 2)
            self.label.setText(f"pow({text}) = {result}")
        except ValueError:
            
            self.label.setText("Invalid input")

    def action_ln(self):
        text = self.label.text()
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.log(value)
            self.label.setText(f"ln({text}) = {result}")
        except ValueError:
            # Якщо текст не можна перетворити в число
            self.label.setText("Invalid input")

    def action_log(self):
        text = self.label.text()
        try:
            # Перетворення тексту в число
            value = float(text)
            # Обчислення косинусу
            result = math.log10(value)
            self.label.setText(f"log({text}) = {result}")
        except ValueError:
            # Якщо текст не можна перетворити в число
            self.label.setText("Invalid input")

# рівяння  X+10=12

#5!= 1*2*3*4*5=120


app = QApplication(sys.argv)
with open('style', 'r') as stule_file:
    style = stule_file.read()
    app.setStyleSheet(style)
window = Window()
sys.exit(app.exec())