from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal,QTimer
from function_class import main_app,sign_in,sign_up,password,intruduce
import json
from time import sleep
import asyncio
def sign_in_():
    window2.close()
    window1.show()
def sign_up_():
    window2.close()
    window3.show()
def password_():
    window2.close()
    window4.show()
def close():
    window5.close()
    window2.show()

app = QApplication([])


window1 = main_app()
window2 = sign_in()
window3 = sign_up()
window4 = password()
window5 = intruduce()



window5.show()

QTimer.singleShot(1100,close)
      


window2.sign_in_signal.connect(sign_in_)
window2.sign_up_signal.connect(sign_up_)
window2.password_signal.connect(password_)







app.exec()

