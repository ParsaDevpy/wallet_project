import requests
from PyQt6.QtWidgets import QMainWindow,QWidget,QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal,QTimer
from threading import Thread
import json
import asyncio
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import database_wallet as data
from models import get_db
import re
from email_function import is_valid_email,send_verification_code
class error(QMainWindow):
    def __init__(self,title,massage):
        super().__init__()
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(massage)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()
class main_app(QMainWindow):
    def __init__(self ):
        super().__init__()

        Form, _ = uic.loadUiType("wallet.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
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
    sign_up_signal = pyqtSignal()
    password_signal = pyqtSignal()
    error_sign = pyqtSignal()
    def __init__(self):
        super().__init__()
        Form, _ = uic.loadUiType("sign in.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(250,230)
        self.ui.pushButton.clicked.connect(self.sign_in)
        self.ui.pushButton_2.clicked.connect(self.sign_up_butten)
        self.ui.pushButton_3.clicked.connect(self.password_butten)
    def sign_in(self):
        db = get_db()
        user = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if db.query(data).filter(data.username == user,data.password == password).all():
            self.sign_in_signal.emit()
        else:
            self.ui.label_3.setText("your password or username is false!!!!")
            self.ui.label_4.setText("your password or username is false!!!!")
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
    def sign_up_butten(self):
        self.sign_up_signal.emit()
    def password_butten(self):
        self.password_signal.emit()
class sign_up(QMainWindow):
    Email_available = pyqtSignal(str,str)
    username_available = pyqtSignal(str,str)
    fill_fields = pyqtSignal(str,str)
    switch_main = pyqtSignal()
    def __init__(self):
        super().__init__()

        Form, _ = uic.loadUiType("sign up.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(270,240)
        self.ui.pushButton.clicked.connect(self.sign_data)
    def sign_data(self):
        db = get_db()
        email_= self.ui.lineEdit_3.text()
        username_ = self.ui.lineEdit.text()
        fullname_ = self.ui.lineEdit_4.text()
        password_ = self.ui.lineEdit_2.text()
        if email_ and username_ and fullname_ and password_ and is_valid_email():
            if db.query(data).filter(data.email == email_).all():
                self.Email_available.emit("sign up error","your email is exis!!")
            elif db.query(data).filter(data.username == username_).all():
                self.username_available.emit("sign up error","your username is not available!!")
            else:
                new_user = data(
                    username = username_,
                    email = email_,
                    fullname = fullname_,
                    password = password_
                )
                db.add(new_user)
                db.commit()
                self.switch_main.emit()
        else:
            self.fill_fields.emit("sign up error","Please fill in all the fields.")
class forgot_password(QMainWindow):
    verifi_error = pyqtSignal(str,str)
    email_error = pyqtSignal(str,str)
    def __init__(self):
        super().__init__()
        Form, _ = uic.loadUiType("password.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(270,220)
        self.ui.pushButton.clicked.connect(self.send_code)
        self.ui.pushButton_2.clicked.connect(self.set_password)
    def send_code(self):
        email_address = self.ui.lineEdit.text()
        if email_address:
            if is_valid_email():
                code = send_verification_code(email_address)
                if code:
                    self.code = code
                    self.ui.label_4.setText("succesful!!")
                    self.ui.pushButton.setEnabled(False)
                    QTimer.singleShot(60000,self.back_butten)
                else:
                    self.verifi_error.emit("connection eroor","try again!!")
            else:
                self.email_error.emit("email error","your email is not available!!")
        else:
            self.email_error.emit("email error","your email is not available!!")
    def back_butten(self):
        self.ui.pushButton.setEnabled(True)
    def set_password(self):
        new_password = self.ui.lineEdit_3.text()
        confirm_code = self.ui.lineEdit_2.text()
        if confirm_code and new_password:
            if confirm_code == self.code:
                pass

class intruduce(QMainWindow):

    def __init__(self):
        super().__init__()
        self.a = 5
        Form, _ = uic.loadUiType("intruduce.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(270,220)

