import sys

from PyQt5.QtGui import QPalette, QFont

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QSpinBox, QPushButton, QVBoxLayout, QHBoxLayout, \
    QLabel, QWidget, QMessageBox

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import random
import threading

label_font = QFont("Times", 16)
btn_font = QFont("Times", 16, QFont.Bold)

site_visited = 1
site_failed = 1

agents = ["Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
           "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
           "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/108.0.5359.112 Mobile/15E148 Safari/604.1",
           "Mozilla/5.0 (iPad; CPU OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/108.0.5359.112 Mobile/15E148 Safari/604.1",
           "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; SM-A102U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; LM-Q720) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.128 Mobile Safari/537.36",
           "Mozilla/5.0 (iPhone; CPU iPhone OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/108.0 Mobile/15E148 Safari/605.1.15",
           "Mozilla/5.0 (iPad; CPU OS 13_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/108.0 Mobile/15E148 Safari/605.1.15",
           "Mozilla/5.0 (Android 13; Mobile; rv:68.0) Gecko/68.0 Firefox/108.0",
           "Mozilla/5.0 (Android 13; Mobile; LG-M255; rv:108.0) Gecko/108.0 Firefox/108.0",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1; rv:108.0) Gecko/20100101 Firefox/108.0",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
           "Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0",
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
           "Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1",
           "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"]


class UserInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Website viewer")
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        #Left side

        left_side = QWidget()
        left_layout = QVBoxLayout()
        left_side.setLayout(left_layout)
        left_side.setStyleSheet("background-color:rgb(40,44,52)")

        self.text_input1 = QLineEdit()
        self.text_input1.setStyleSheet("min-height:30px;border-radius:5px;border:1px solid #999999;padding-left:10px;color:white;")
        self.text_input1.setPlaceholderText("Link One")
        left_layout.addWidget(self.text_input1)

        self.text_input2 = QLineEdit()
        self.text_input2.setStyleSheet(
            "min-height:30px;border-radius:5px;border:1px solid #999999;padding-left:10px;color:white;")
        self.text_input2.setPlaceholderText("Link One")
        left_layout.addWidget(self.text_input2)

        self.text_input3 = QLineEdit()
        self.text_input3.setStyleSheet(
            "min-height:30px;border-radius:5px;border:1px solid #999999;padding-left:10px;color:white;")
        self.text_input3.setPlaceholderText("Link One")
        left_layout.addWidget(self.text_input3)

        self.button = QPushButton("Start")
        self.button.setStyleSheet("min-height:40px;border-radius:10px;background-color:darkred;")
        self.button.setFont(btn_font)
        self.button.clicked.connect(self.start)
        palette = self.button.palette()
        palette.setColor(QPalette.ButtonText, Qt.white)
        self.button.setPalette(palette)
        left_layout.addWidget(self.button)

        #Right side

        right_side = QWidget()
        right_layout = QVBoxLayout()
        right_side.setLayout(right_layout)
        right_side.setStyleSheet("background-color:rgb(51,56,56)")

        self.label1 = QLabel("Site viewed: 1002")
        self.label1.setStyleSheet("color:white")
        self.label1.setFont(label_font)
        right_layout.addWidget(self.label1)

        self.label2 = QLabel("Site failed: 3")
        self.label2.setStyleSheet("color:white")
        self.label2.setFont(label_font)
        right_layout.addWidget(self.label2)

        #Main

        main_layout.addWidget(left_side, stretch=7)
        main_layout.addWidget(right_side, stretch=3)

        self.setCentralWidget(main_widget)
        self.show()
        self.resize(700, 500)

    def load_proxies(self, path):
        return open(path).read().split('\n')

    def load_session(self, proxy):
        proxy, port = proxy.split(':')
        id = random.randrange(0, len(agents))
        agent = agents[id]
        options = Options()
        options.set_preference("network.proxy.type", 1)
        options.set_preference("network.proxy.http", proxy)
        options.set_preference("network.proxy.type_port", port)
        options.set_preference("network.proxy.ssl", proxy)
        options.set_preference("network.proxy.ssl_port", port)
        options.set_preference("general.useragent.override", agent)
        options.headless = True

        driver = webdriver.Firefox(options=options)

        try:
            driver.get(self.text_input1.text())
            time.sleep(3)
            driver.refresh()
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.get(self.text_input2.text())
            time.sleep(3)
            driver.refresh()
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            driver.get(self.text_input3.text())
            time.sleep(3)
            driver.refresh()
            time.sleep(2)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.quit()
        except:
            driver.quit()
            raise Exception("Failed to load website")

    def main(self):
        global site_visited
        global site_failed
        proxies = self.load_proxies("proxies.txt")

        while True:
            id = random.randrange(0, len(proxies))
            proxy = proxies[id]
            try:
                self.load_session(proxy)
                print("View counted:", site_visited)
                self.label1.setText("Site visited: {}".format(site_visited))
                site_visited += 1
            except Exception as e:
                self.label2.setText("Site failed: {}".format(site_failed))
                site_failed += 1
                print("View failed:", site_failed)
                print(e)

    def start(self):
        if not self.text_input1.text() or not self.text_input2.text() or not self.text_input3.text() :
            message = QMessageBox()
            message.setWindowTitle("Input Error")
            message.setText("Please fill in all input fields.")
            message.exec_()
        else:
            #print("All right")
            thread = threading.Thread(target=self.main)
            thread.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UserInterface()
    ui.show()
    sys.exit(app.exec_())