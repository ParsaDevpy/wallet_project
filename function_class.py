import requests
from PyQt6.QtWidgets import QApplication
from threading import Thread
from PyQt6 import uic
import json
class main_app(QApplication):
    def __init__(self, argv:list):
        super().__init__(argv)

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
        app = QApplication([])
        window = Window()
        form = Form()
        form.setupUi(window)
        window.setFixedSize(241,170)
        price_thread = Thread(target=update_price)
        price_thread.start()

        form.comboBox.addItems(['BTCIRT','ETHIRT','USDTIRT'])



        window.show()
        app.exec()
class sign_up_in(QApplication):
    def __init__(self, argv:list):
        super().__init__(argv)
        global text
        text = []
        def sign_in():
            global text
            text.append(form.lineEdit.text())
            text .append(form.lineEdit_2.text())
            form.lineEdit.setText("")
            form.lineEdit_2.setText("")

        def sign_up_butten():
            d = {"check":"sign_up"}
            with open("word.json","w") as file:
                json.dump(d,file)
            app.exit()    
        Form, Window = uic.loadUiType("sign up_in.ui")
        app = QApplication([])
        window = Window()
        form = Form()
        form.setupUi(window)
        window.setFixedSize(241,205)

        form.pushButton.clicked.connect(sign_in)
        form.pushButton_2.clicked.connect(sign_up_butten)
 

        window.show()
        app.exec()

