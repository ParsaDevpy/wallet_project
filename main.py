from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from time import sleep
from PyQt6.QtWidgets import QWidget,QApplication,QLabel
from threading import Thread
from function_class import nobitex
class main_app(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

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








