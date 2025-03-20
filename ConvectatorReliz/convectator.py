import sys
import requests
from PyQt5.QtWidgets import*

CONVERSION_RATES = {
     "Centimetres": 0.01,
     "Metres": 1.0,
     "Millimitres": 0.001,
     "Kilometres": 1000.0
}

CONVERSION_RATES_v = {
     "Centilitres": 0.01,
     "Litres": 1.0,
     "Millilitres": 0.001,
     "Hectolitres": 1000.0
}

class UnitsofmeasuementConvetor(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Конверкатор одиниць виміру")
        self.setGeometry(100, 100, 600, 500)
        
    ###довжини
        self.amount_label = QLabel("Число:", self)
        self.amount_input = QLineEdit(self)
        
        self.from_Unitsofmeasuement__label = QLabel("З якої одиниці виміру:", self)    
        self.from_Unitsofmeasuement = QComboBox(self)
        self.from_Unitsofmeasuement.addItems(["Centimetres", "Metres", "Millimetres", "Kilometres"])    
        
        self.to_Unitsofmeasuement_label = QLabel("У яку одиницю виміру:", self)    
        self.to_Unitsofmeasuement = QComboBox(self)
        self.to_Unitsofmeasuement.addItems(["Centimetres", "Metres", "Millimetres", "Kilometres"]) 
        
        self.convert_button = QPushButton("Конвертувати", self)
        self.convert_button.clicked.connect(self.convert_units)
        
        self.result_label = QLabel("", self)

###об'єм
        self.amount_label_v = QLabel("Число:", self)
        self.amount_input_v = QLineEdit(self)

        self.from_v_label = QLabel("З якої одиниці об'єму:", self)    
        self.from_v = QComboBox(self)
        self.from_v.addItems(["Centilitres", "Litres", "Millilitres", "Hectolitres"]) 

        self.to_v_label = QLabel("У яку одиницю об'єму:", self)    
        self.to_v = QComboBox(self)
        self.to_v.addItems(["Centilitres", "Litres", "Millilitres", "Hectolitres"]) 
        
        self.convert_button_v = QPushButton("Конвертувати", self)
        self.convert_button_v.clicked.connect(self.convert_units_v)
        
        self.result_label_v = QLabel("", self)

###довжини    
        layout = QVBoxLayout()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.from_Unitsofmeasuement__label)
        layout.addWidget(self.from_Unitsofmeasuement)
        
        layout.addWidget(self.to_Unitsofmeasuement_label)
        layout.addWidget(self.to_Unitsofmeasuement)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label)

###об'єми
        layout.addWidget(self.amount_label_v)
        layout.addWidget(self.amount_input_v)
        layout.addWidget(self.from_v_label)
        layout.addWidget(self.from_v)
        
        layout.addWidget(self.to_v_label)
        layout.addWidget(self.to_v)
        layout.addWidget(self.convert_button_v)
        layout.addWidget(self.result_label_v)
        
        self.setLayout(layout)

        
    def convert_units(self):
        try:
            amount = float(self.amount_input.text())
            from_unit = self.from_Unitsofmeasuement.currentText()
            to_unit = self.to_Unitsofmeasuement.currentText()

            if from_unit == to_unit:
                self.result_label.setText("Виберіть різні одиниці виміру")
                return

            amount_in_metres = amount * CONVERSION_RATES[from_unit]
            converted_amount = amount_in_metres / CONVERSION_RATES[to_unit]

            self.result_label.setText(f"{amount} {from_unit} = {converted_amount:1f} {to_unit}")
            print(converted_amount)
        except  ValueError:
            self.result_label.setText("Некоректне значення") 


    def convert_units_v(self):
        try:
            amount_v = float(self.amount_input_v.text())
            from_unit_v = self.from_v.currentText()
            to_unit_v = self.to_v.currentText()

            if from_unit_v == to_unit_v:
                self.result_label_v.setText("Виберіть різні одиниці виміру")
                return

            amount_in_metres_v = amount_v * CONVERSION_RATES_v[from_unit_v]
            converted_amount_v = amount_in_metres_v / CONVERSION_RATES_v[to_unit_v]

            self.result_label_v.setText(f"{amount_v} {from_unit_v} = {converted_amount_v:1f} {to_unit_v}")
            print(converted_amount_v)
        except  ValueError:
            self.result_label_v.setText("Некоректне значення") 


app = QApplication(sys.argv)

with open('style', 'r') as style_file:
    style = style_file.read()
    app.setStyleSheet(style)

window = UnitsofmeasuementConvetor()
window.show()
sys.exit(app.exec_())