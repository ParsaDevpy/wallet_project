import requests
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from threading import Thread
import json
class main_app(QMainWindow):
    def __init__(self ):
        super().__init__()

        Form, _ = uic.loadUiType("wallet.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setFixedSize(241,170)
        price_thread = Thread(target=self.update_price)
        price_thread.start()

        self.ui.comboBox.addItems(['BTCIRT','ETHIRT','USDTIRT'])

    def nobitex(self,IRT):
        r = requests.get(f"https://apiv2.nobitex.ir/v3/orderbook/{IRT}IRT")
        data = r.json()

        if data["status"] == 'ok' :
            price = data['lastTradePrice']
            price = price[:-1]
            
        else:
            price = 404

        return price 

    def update_price(self):
        while True:
            self.ui.label_4.setText(f'{self.nobitex("USDT")} تومان')
            self.ui.label_5.setText(f'{self.nobitex("ETH")} تومان')
            self.ui.label_6.setText(f'{self.nobitex("BTC")} تومان')
            self.ui.label_4.setText(f'{self.nobitex("USDT")} تومان')
            self.ui.label_5.setText(f'{self.nobitex("ETH")} تومان')
            self.ui.label_6.setText(f'{self.nobitex("BTC")} تومان')

class sign_in(QMainWindow):
    sign_in_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.text = []
   
        Form, _ = uic.loadUiType("sign in.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setFixedSize(241,205)

        self.ui.pushButton.clicked.connect(self.sign_in)
        self.ui.pushButton_2.clicked.connect(self.sign_up_butten)
    def sign_in(self):
        self.sign_in_signal.emit()
        # self.text.append(self.ui.lineEdit.text())
        # self.text .append(self.ui.lineEdit_2.text())
        # self.ui.lineEdit.setText("")
        # self.ui.lineEdit_2.setText("")

    def sign_up_butten(self):
        d = {"check":"sign_up"}
        with open("word.json","w") as file:
            json.dump(d,file)
class sign_up(QMainWindow):
    def __init__(self):
        super().__init__()

        Form, _ = uic.loadUiType("sign up.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setFixedSize(270,240)

class password(QMainWindow):
    def __init__(self):
        super().__init__()

        Form, _ = uic.loadUiType("password.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setFixedSize(270,220)