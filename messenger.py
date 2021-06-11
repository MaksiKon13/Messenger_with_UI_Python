from datetime import datetime

import requests
from PyQt6 import QtWidgets, QtCore

import clientui


class Messenger(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self, host):
        super().__init__()
        self.setupUi(self)

        self.host = host   # это для подключения к внешнему хосту ngrok)

        self.pushButton.pressed.connect(self.send_message)  # button for send message
        self.after = 0  # Создание переменной after для опроса сервера на наличие новых сообщений (метод get_messages)
        # создание таймера для вызова метода
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(5000)

    def show_messages(self, messages):
        for message in messages:
            dt = datetime.fromtimestamp(message['time'])
            self.textBrowser.append(dt.strftime('%H:%M:%S') + ' ' + message['name'])
            self.textBrowser.append(message['text'])
            self.textBrowser.append('')

    def get_messages(self):
        try:
            response = requests.get(
                url=self.host + '/messages',
                params={'after': self.after}
            )
            print(response)
        except:
            return

        messages = response.json()['messages']
        if messages:
            self.show_messages(messages)
            self.after = messages[-1]['time']

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post(
                url=self.host + '/send',
                json={'name': name, 'text': text}
            )

        except:
            self.textBrowser.append('Сервер недоступен')  # TODO
            self.textBrowser.append(' ')
            return
        if response != 200:
            self.textBrowser.append('Неправильное имя или текст')  # TODO
            self.textBrowser.append(' ')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = Messenger('http://4c70f3f543bd.ngrok.io')
window.show()
app.exec()
