from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal,QTimer
from function_class import main_app,sign_in,sign_up,password,intruduce
import json
from models import Base,database_wallet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
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
Engine = create_engine("sqlite:///database_wallet.db", echo=True)
sessionlocal = sessionmaker(bind=Engine)
if os.path.isfile("database_wallet.db"):
    pass
else:
    Base.metadata.create_all(Engine)



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

