from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal
from function_class import main_app,sign_in,sign_up,password
import json



app = QApplication([])


def check(window_1,window_2):
    window_1.close()
    window_2.show()  
      

window1 = main_app()
window2 = sign_in()
window3 = sign_up()
window4 = password()




window2.sign_in_signal.connect(check)

window2.show()
app.exec()

