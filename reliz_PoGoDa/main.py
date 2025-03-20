import sys
import requests
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QGraphicsView, QGraphicsScene, QTextEdit)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import *
import matplotlib.dates as mdates
import datetime
import matplotlib.backends.backend_qt5agg as qt5agg

API_KEY = "f81703c1f3b81ad93e6644153c4a426e"
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?appid={}&units=metric&lang=ua&q={}"
HISTORY_FILE = "history.txt"

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("(._((._(Погода)_.))_.)")
        self.setGeometry(100, 100, 1000, 900)
        self.layout = QVBoxLayout()

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Введіть назву міста")
        self.city_input.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.city_input)

        self.weather_label = QLabel("Введіть місто та натисніть кнопку", self)
        self.weather_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.weather_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.weather_label)

        self.temp_label = QLabel("", self)
        self.layout.addWidget(self.temp_label)
        self.pressure_label = QLabel("", self)
        self.layout.addWidget(self.pressure_label)
        self.humidity_label = QLabel("", self)
        self.layout.addWidget(self.humidity_label)
        self.wind_label = QLabel("", self)
        self.layout.addWidget(self.wind_label)

        self.refresh_button = QPushButton("Оновити", self)
        self.refresh_button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.refresh_button)

        self.history_button = QPushButton("Історія пошуку", self)
        self.history_button.clicked.connect(self.show_history)
        self.layout.addWidget(self.history_button)

        self.graph_view = QGraphicsView(self)
        self.graph_scene = QGraphicsScene(self.graph_view)
        self.graph_view.setScene(self.graph_scene)
        self.layout.addWidget(self.graph_view)

        self.setLayout(self.layout)

    def get_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.weather_label.setText("Будь ласка, введіть назву міста.")
            return

        url = BASE_URL.format(API_KEY, city)
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == "200":
                temp = round(data["list"][0]["main"]["temp"], 1)
                pressure = data["list"][0]["main"]["pressure"]
                humidity = data["list"][0]["main"]["humidity"]
                wind_speed = round(data["list"][0]["wind"]["speed"], 1)
                weather = data["list"][0]["weather"][0]["description"].capitalize()

                self.weather_label.setText(f"Погода в місті {city}: {weather}")
                self.temp_label.setText(f"🌡 Температура: {temp}°C")
                self.pressure_label.setText(f"🌬 Тиск: {pressure} гПа")
                self.humidity_label.setText(f"💧 Вологість: {humidity}%")
                self.wind_label.setText(f"💨 Швидкість вітру: {wind_speed} м/с")

                self.save_to_history(city)
                self.plot_temperature(data)
        except Exception as e:
            self.show_error_message("Помилка отримання даних.")
            print(e)

    def plot_temperature(self, data):
        time_data = []
        temp_data = []
        for forecast in data["list"][:12]:
            time_data.append(datetime.datetime.strptime(forecast["dt_txt"], "%Y-%m-%d %H:%M:%S"))
            temp_data.append(forecast["main"]["temp"])

        plt.figure(figsize=(8, 5))
        plt.plot(time_data, temp_data, marker='o', color='b')
        plt.title("Прогноз температури")
        plt.xlabel("Час")
        plt.ylabel("Температура (°C)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:00'))

        canvas = qt5agg.FigureCanvasQTAgg(plt.gcf())
        self.graph_scene.clear()
        self.graph_scene.addWidget(canvas)
        canvas.draw()

    def save_to_history(self, city):
        with open(HISTORY_FILE, "a") as file:
            file.write(city + "\n")

    def show_history(self):
        self.history_window = HistoryWindow()
        self.history_window.show()

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Помилка")
        msg.setText(message)
        msg.exec_()

class HistoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Історія пошуку")
        self.setGeometry(200, 200, 400, 400)
        layout = QVBoxLayout()

        self.history_text = QTextEdit(self)
        self.history_text.setReadOnly(True)
        layout.addWidget(self.history_text)

        self.load_history()
        self.setLayout(layout)

    def load_history(self):
        try:
            with open(HISTORY_FILE, "r") as file:
                lines = file.readlines()
                last_entries = lines[-10:]
                self.history_text.setText("".join(last_entries))
        except FileNotFoundError:
            self.history_text.setText("Історія поки що порожня.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    file = QFile("style")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    file.close()

    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())