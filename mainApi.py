#a whether api i built using a tutorial that i havent finished for 2months.i hate myself.
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QVBoxLayout,QLineEdit
import requests
from PyQt5.QtCore import Qt
class whetherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter city name:",self)
        self.city_input=QLineEdit(self)
        self.get_whether_btn=QPushButton("Get Whether",self)
        self.temp_label=QLabel("",self)
        self.whether_emoji_label=QLabel("",self)
        self.description_label=QLabel("")
        self.city_input.setPlaceholderText("for eg: pokhara..")
        self.get_whether_btn.clicked.connect(self.get_whether)
        self.inUI()

    def inUI(self):
        #main window UI
        self.setWindowTitle("Whether App")
        self.setGeometry(700,300,350,400)

    #label & btn UI
        vbox=QVBoxLayout(self)
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_whether_btn)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.whether_emoji_label)
        vbox.addWidget(self.description_label)
        vbox.setAlignment(Qt.AlignTop)
        #centering stuff
        self.city_label.setAlignment(Qt.AlignHCenter)
        self.city_input.setAlignment(Qt.AlignHCenter)
        self.temp_label.setAlignment(Qt.AlignHCenter)
        self.whether_emoji_label.setAlignment(Qt.AlignHCenter)
        self.description_label.setAlignment(Qt.AlignHCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_whether_btn.setObjectName("get_whether_btn")
        self.temp_label.setObjectName("temp_label")
        self.whether_emoji_label.setObjectName("whether_emoji_label")
        self.description_label.setObjectName("description_label")

        #some css 
        self.setStyleSheet("""
        QLabel,QPushButton,QLineEdit{
        font-family:calibri;
        }
        QLabel#city_label{
        font-size:40px;
        }
        QLineEdit#city_input{
        border:2px solid grey;
        border-radius:12px;
        height:50px;
        font-size:25px;
        }
        QPushButton#get_whether_btn{
        border:1px solid grey;
        border-radius:6px;
        height:30px;
        font-size:25px;
        }
        QLabel#temp_label{
        font-size:50px;
        font-weight:500;
        }
        QLabel#whether_emoji_label{
        font-size:80px;
        font-family:Segoe UI emoji;
        }
        QLabel#description_label{
        font-size:35px;
        font-weight:300;
        }
        """)

    def get_whether(self):
        api_key="bd7775deda23f8196cf798cd0adea518"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()
            self.display_whether(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_errors("Bad Request: \nCheck Your Input")
                case 401:
                    self.display_errors("Unauthorized Access: \nInvalid Api Key")
                case 403:
                    self.display_errors("Forbidden: \nAccess is denied")
                case 404:
                    self.display_errors("Not found:\nCity not found")
                case 500:
                    self.display_errors("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_errors("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_errors("Service Unavailable:\nServer is down")
                case 504:
                    self.display_errors("Gateway Timeout: \nNo response from the server")
                case _:
                    self.display_errors(f"HTTP error occured \n {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_errors("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_errors("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_errors("Too many redirects\n Check the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_errors(f"Request Error:\n{req_error}")

    def display_errors(self,msg):
        self.description_label.setText("")
        self.whether_emoji_label.setText("")
        self.temp_label.setStyleSheet("font-size:30px;color:red;font-weight:300")
        self.temp_label.setText(msg)

    def display_whether(self,data):
        self.temp_label.setStyleSheet("font-size:50px;color:black;font-weight:500")
        temp_k=data["main"]["temp"]
        temp_c=temp_k-273.15
        temp_f=(temp_c*9/5)+32
        weather_description=data["weather"][0]["description"]
        weather_id=data["weather"][0]["id"]

        self.description_label.setText(weather_description)
        self.temp_label.setText(f"{int(temp_f)}°F / {int(temp_c)}°C")
        self.whether_emoji_label.setText(self.get_whether_emoji(weather_id))
    @staticmethod
    def get_whether_emoji(w_id):
        if 200<=w_id<=232:
            return "⛈️"
        elif 300<=w_id<=321:
            return "🌦️"
        elif 500<=w_id<=531:
            return "🌧️"
        elif 600<=w_id<=622:
            return "❄️"
        elif 701<=w_id<=741:
            return "🍃"
        elif w_id==762:
            return "🌋"
        elif w_id==771:
            return "💨"
        elif w_id == 781:
            return "🌪️"
        elif w_id == 800:
            return "☀️"
        elif 801<= w_id <=804:
            return "🌥️"
        else:
            return "❓"
if __name__=="__main__":
    app=QApplication(sys.argv)
    whetherWindow=whetherApp()
    whetherWindow.show()
    sys.exit(app.exec_())
