from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal,QTimer
from function_class import main_app,sign_in,sign_up,forgot_password,intruduce,error
import json
from models import Base,database_wallet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
def switch_window(win1,win2):
    win1.close()
    win2.show()
def show_error(title,massage):
    msg = error(title,massage)

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
window4 = forgot_password()
window5 = intruduce()



window5.show()

QTimer.singleShot(1100,lambda: switch_window(window5,window2))
      


window2.sign_in_signal.connect(lambda: switch_window(window2,window1))
window2.sign_up_signal.connect(lambda: switch_window(window2,window3))
window2.password_signal.connect(lambda: switch_window(window2,window4))
window3.Email_available.connect(show_error)
window3.username_available.connect(show_error)
window3.fill_fields.connect(show_error)
window3.switch_main.connect(lambda: switch_window(window3,window1))




app.exec()

