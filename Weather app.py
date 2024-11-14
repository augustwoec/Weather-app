import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class weatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperatuer_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.discription_label = QLabel(self)
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperatuer_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.discription_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperatuer_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.discription_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("City_label")
        self.city_input.setObjectName("City_input")
        self.get_weather_button.setObjectName("Get_weather_button")
        self.temperatuer_label.setObjectName("Temperatuer_label")
        self.emoji_label.setObjectName("emoji_label")
        self.discription_label.setObjectName("Discription_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperatuer_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#discription_label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        
        api_key = "af692c304ce4d2ec2bd49c637851768c"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nPlease try agian later")
                case 502:
                    self.display_error("Bad gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured\n{http_error}")
                    
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.display_error("Timeout error\nThe requests timed out")

        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")



    def display_error(self, message):
        self.temperatuer_label.setStyleSheet("font-size: 30px;")
        self.temperatuer_label.setText(message)
        self.emoji_label.clear()
        self.discription_label.clear()
        
    def display_weather(self, data):
        self.temperatuer_label.setStyleSheet("font-size: 30px;")
        temp_k = data["main"]["temp"] 
        temp_c = temp_k - 273.15
        weather_id = data["weather"][0]["id"]
        weather_discription = data["weather"][0]["description"]

        self.temperatuer_label.setText(f"{temp_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.discription_label.setText(weather_discription)

    @staticmethod            
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "🌩"
        elif 300 <= weather_id <= 321:
            return "⛅️"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "⛄️"
        elif 701 <= weather_id <= 741:
            return "🌁"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "🌥"
        
    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = weatherApp()
    weather_app.show()
    sys.exit(app.exec_())