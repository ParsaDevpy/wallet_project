import requests
from PyQt6.QtWidgets import QMainWindow,QWidget
from threading import Thread
from PyQt6 import uic
import json
class main_app(QWidget):
    def __init__(self ):
        super().__init__()

        def nobitex(IRT):
            r = requests.get(f"https://apiv2.nobitex.ir/v3/orderbook/{IRT}IRT")
            data = r.json()

            if data["status"] == 'ok' :
                price = data['lastTradePrice']
                price = price[:-1]
                
            else:
                price = 404

            return price 

        def update_price():
            while True:
                form.label_4.setText(f'{nobitex("USDT")} تومان')
                form.label_5.setText(f'{nobitex("ETH")} تومان')
                form.label_6.setText(f'{nobitex("BTC")} تومان')
                form.label_4.setText(f'{nobitex("USDT")} تومان')
                form.label_5.setText(f'{nobitex("ETH")} تومان')
                form.label_6.setText(f'{nobitex("BTC")} تومان')



        Form, Window = uic.loadUiType("wallet.ui")
        window = Window()
        form = Form()
        form.setupUi(window)
        window.setFixedSize(241,170)
        # price_thread = Thread(target=update_price)
        # price_thread.start()

        form.comboBox.addItems(['BTCIRT','ETHIRT','USDTIRT'])




class sign_up_in(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text = []
   
        Form, _ = uic.loadUiType("sign up_in.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setFixedSize(241,205)

        self.ui.pushButton.clicked.connect(self.sign_in)
        self.ui.pushButton_2.clicked.connect(self.sign_up_butten)
    def sign_in(self):
        self.text.append(self.ui.lineEdit.text())
        self.text .append(self.ui.lineEdit_2.text())
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")

    def sign_up_butten(self):
        d = {"check":"sign_up"}
        with open("word.json","w") as file:
            json.dump(d,file)


