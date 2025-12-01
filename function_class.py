
from PyQt6.QtWidgets import QMainWindow,QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal,QTimer
from PyQt6.QtGui import QPixmap
from threading import Thread
import requests
import json
import pandas as pd
import plotly.graph_objects as go
from models import database_wallet as data
from models import get_db
from email_function import is_valid_email,send_verification_code,send_email_to_manage

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
    connect_error = pyqtSignal(str,str)
    switch_window = pyqtSignal()
    BTC_chart = pyqtSignal()
    ETH_chart = pyqtSignal()
    USDT_chart = pyqtSignal()
    def __init__(self ):
        super().__init__()

        Form, _ = uic.loadUiType("wallet.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(241,220)
        self.ui.pushButton_3.clicked.connect(self.transaction)
        self.ui.pushButton_4.clicked.connect(self.transaction)
        self.ui.pushButton.clicked.connect(self.update_balance)
        self.ui.pushButton_2.clicked.connect(self.buy)
        self.ui.pushButton_1.clicked.connect(self.sell)
        self.ui.pushButton_5.clicked.connect(self.chart)

        
        price_thread = Thread(target=self.update_price)
        price_thread.start()
        self.ui.comboBox.addItems(['BTC','ETH','USDT'])
        self.ui.comboBox_2.addItems(['BTC','ETH','USDT'])
    def nobitex(self,IRT):
        try:
            r = requests.get(f"https://apiv2.nobitex.ir/v3/orderbook/{IRT}IRT")
            data = r.json()

            if data["status"] == 'ok' :
                price = data['lastTradePrice']
                price = price[:-1]
                
            else:
                price = 404

            return price 
        except:
            self.connect_error.emit("connection error","check your internet and try again.")

    def update_price(self):
        try:
            while True:
                self.ui.label_4.setText(f'{self.nobitex("USDT")} تومان')
                self.ui.label_5.setText(f'{self.nobitex("ETH")} تومان')
                self.ui.label_6.setText(f'{self.nobitex("BTC")} تومان')
                self.ui.label_4.setText(f'{self.nobitex("USDT")} تومان')
                self.ui.label_5.setText(f'{self.nobitex("ETH")} تومان')
                self.ui.label_6.setText(f'{self.nobitex("BTC")} تومان')
        except:
            self.connect_error.emit("error","error in update price")
    def update_balance(self):
        try:
            db = get_db()
            with open("user.json","r") as f:
                balance = json.load(f)
            result = db.query(data).filter(data.username == balance["user"]).first()
            self.ui.label_9.setText(f"IRT: {result.IRT}")
            self.ui.label_10.setText(f"BTC: {result.BTC}")
            self.ui.label_8.setText(f"ETH: {result.ETH}")
            self.ui.label_11.setText(f"USDT: {result.USDT}")
        except:
            self.connect_error.emit("database error","try again.")
    def buy(self):
        try:
            db = get_db()
            with open("user.json","r") as f:
                balance = json.load(f)
            result = db.query(data).filter(data.username == balance["user"]).first()
            amount = float(self.ui.lineEdit.text())
            Currency = self.ui.comboBox.currentText()
            price = float(self.nobitex(Currency))
            main_price = price * amount
            result_IRT = float(result.IRT)
            result_Currency = float(getattr(result,Currency))
            if main_price <= result_IRT:
                result_IRT -= main_price
                result_Currency += amount
                setattr(result,Currency,result_Currency)
                result.IRT = result_IRT
                db.commit()
                self.ui.label_13.setText("succesful!")
                self.update_balance()
            else:
                self.connect_error.emit("error","you don't have enough money!!")
        except:
            self.connect_error.emit("database error","try again.")
    def sell(self):
        try:
            db = get_db()
            with open("user.json","r") as f:
                balance = json.load(f)
            result = db.query(data).filter(data.username == balance["user"]).first()
            amount = float(self.ui.lineEdit.text())
            Currency = self.ui.comboBox.currentText()
            price = float(self.nobitex(Currency))
            main_price = price * amount
            result_IRT = float(result.IRT)
            result_Currency = float(getattr(result,Currency))
            if amount <= result_Currency:
                result_IRT += main_price
                result_Currency -= amount
                setattr(result,Currency,result_Currency)
                result.IRT = result_IRT
                db.commit()
                self.ui.label_13.setText("succesful!")
                self.update_balance()
            else:
                self.connect_error.emit("error","you don't have enough money!!")
        except:
            self.connect_error.emit("database error","try again.")
    def chart(self):
        try:

            Currency_chart = self.ui.comboBox_2.currentText()
            match Currency_chart:
                case "USDT":
                    self.USDT_chart.emit()
                case "BTC":
                    self.BTC_chart.emit()
                case "ETH":
                    self.ETH_chart.emit()
        except:
            self.connect_error.emit("database error","try again.")
    def transaction(self):
        self.switch_window.emit()

class deposit_withdraw(QMainWindow):
    balane_error = pyqtSignal(str,str)
    fill_fields = pyqtSignal(str,str)
    def __init__(self):
        super().__init__()      
        Form, _ = uic.loadUiType("deposite_withfraw.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(243,275)
        self.ui.pushButton.clicked.connect(self.withdraw)
        self.ui.pushButton_2.clicked.connect(self.deposite)
    def withdraw(self):
        try:

            db = get_db()
            email = self.ui.lineEdit_4.text()
            username = self.ui.lineEdit_3.text()
            Amount = self.ui.lineEdit_2.text()
            card_number = self.ui.lineEdit.text()
            check_email = db.query(data).filter(data.email == email).first()
            if email and username and Amount and card_number and check_email:
                if check_email.username == username:
                    if int(Amount) <= check_email.balance:
                        result = send_email_to_manage(f"کاربر به ایمیل و نام کاربری {email},{username} درخواست برداشت {Amount} تومان به شماره ی {card_number} را دارد.","درخواست برداشت")
                        if result:
                            self.ui.label_8.setText(result)
                        else:
                            self.fill_fields.emit("connection error","Please try again.")
                    else:
                        self.balane_error.emit("balance error","The requested amount is less than your balance.")
                else:
                    self.fill_fields.emit("error","Please fill in all the fields correct.")
            else:
                self.fill_fields.emit("error","Please fill in all the fields correct.")
        except:
            self.fill_fields.emit("connection error","Please try again.")
    def deposite(self):
        try:
            db = get_db()
            email = self.ui.lineEdit_5.text()
            username = self.ui.lineEdit_6.text()
            massage = self.ui.textEdit.toPlainText()
            check_email = db.query(data).filter(data.email == email).first()
            if email and username and massage and check_email:
                if check_email.username == username:
                    result = send_email_to_manage(f"کاربر به ایمیل و نام کاربری {email},{username} درخواست واریزی دارد رسید واریزی: {massage}","درخواست واریز")
                    if result:
                        self.ui.label_9.setText(result)
                    else:
                        self.fill_fields.emit("connection error","Please try again.")
                else:
                    self.fill_fields.emit("error","Please fill in all the fields correct.")
            else:
                self.fill_fields.emit("error","Please fill in all the fields correct.")
        except:
            self.fill_fields.emit("connection error","Please try again.")
class chart(QMainWindow):
    connection_Error = pyqtSignal(str,str)
    def __init__(self,coin):
        super().__init__()
        Form, _ = uic.loadUiType("chart.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(621,462)
        self.coin = coin
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.start(30000)
        try:
            self.update_chart()
        except:
            self.connection_Error.emit("connection error","Please try again.")
    def get_price(self):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{self.coin}/market_chart"
            params = {"vs_currency": "usd", "days": 15}
            response = requests.get(url,params)
            data = response.json()
            price = data["prices"]
            df = pd.DataFrame(price,columns=["Timestamp", "Price"])
            df["Data"] = pd.to_datetime(df["Timestamp"], unit="ms")
        except:
            self.connection_Error.emit("connection error","Please try again.")

        return df
    
    def simulate_candeles(self,df):
        try:
            candele = []
            for i in range(0,len(df),5):
                chuck = df.iloc[i:i+5]
                if len(chuck) == 0:
                    continue
                o = chuck["Price"].iloc[0]
                c = chuck["Price"].iloc[-1]
                h = chuck["Price"].max()
                l = chuck["Price"].min()
                t = chuck["Data"].iloc[0]
                candele.append([t,o,c,h,l])
                df_candele = pd.DataFrame(candele,columns=["Date","Open","High","Low","Close"])
        except:
            self.connection_Error.emit("connection error","Please try again.")
        return df_candele
    def creat_candele(self,df):
        try:
            fig = go.Figure(data=[go.Candlestick(
                x=df["Date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"]
            )])
            fig.write_image("chart.png")
        except:
            self.connection_Error.emit("connection error","Please try again.")
    def update_chart(self):
        df_price = self.get_price()
        df_candele = self.simulate_candeles(df_price)
        self.creat_candele(df_candele)
        pixmap = QPixmap("chart.png")
        self.ui.label.setPixmap(pixmap)
        

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
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        try:
            user = db.query(data).filter(data.username == username,data.password == password).first()
            if user:
                dic = {"user" : username}
                with open("user.json","w") as f:
                    json.dump(dic,f)
                self.sign_in_signal.emit()
            else:
                self.ui.label_3.setText("your password or username is false!!!!")
                self.ui.label_4.setText("your password or username is false!!!!")
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
        except:
            self.ui.label_3.setText("Error while checking login!!!")
            self.ui.label_4.setText("please try again.")


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
        try:
            if email_ and username_ and fullname_ and password_ and is_valid_email(email_):
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
                self.fill_fields.emit("sign up error","Please fill in all the fields correct.")
        except:
            self.fill_fields.emit("data base error","please try agin.")

class forgot_password(QMainWindow):
    verifi_error = pyqtSignal(str,str)
    email_error = pyqtSignal(str,str)
    switch_sign_in = pyqtSignal()

    def __init__(self):
        super().__init__()
        Form, _ = uic.loadUiType("password.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(265,230)

        self.ui.pushButton.clicked.connect(self.send_code)
        self.ui.pushButton_2.clicked.connect(self.set_password)

    def send_code(self):
        self.email_address = self.ui.lineEdit.text()
        try:
            db = get_db()
            email_in_db = db.query(data).filter(data.email == self.email_address).all()
            if self.email_address and is_valid_email(self.email_address) and email_in_db:
                code = send_verification_code(self.email_address)
                if code:
                    self.code = code
                    self.ui.label_4.setText("send it.")
                    self.ui.pushButton.setEnabled(False)
                    QTimer.singleShot(60000,self.back_butten)
                else:
                    self.verifi_error.emit("connection eroor","try again!!")
            else:
                self.email_error.emit("email error","your email is not available!!")
        except:
            self.email_error.emit("error","please check your connection and try again.")
    def back_butten(self):
        self.ui.pushButton.setEnabled(True)

    def set_password(self):
        db = get_db()
        new_password = self.ui.lineEdit_3.text()
        confirm_code = self.ui.lineEdit_2.text()

        if confirm_code and new_password:
            if confirm_code == self.code:
                change_data = db.query(data).filter(data.email == self.email_address).first()
                change_data.password = new_password
                db.commit()
                self.ui.label_4.setText("succesful.")
                self.switch_sign_in.emit()

class intruduce(QMainWindow):

    def __init__(self):
        super().__init__()
        self.a = 5
        Form, _ = uic.loadUiType("intruduce.ui")
        self.ui = Form()
        self.ui.setupUi(self)
        self.setWindowTitle("WALLET APP")
        self.setFixedSize(270,220)

