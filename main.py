from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from function_class import main_app,sign_up_in,sign_up,password
import json



app = QApplication([])


def check():
    with open("word.json","r") as f:
        check_json = json.load(f)["check"]
    if check_json == "sign_up":
        window1.close()
        window2.show()  
      

window1 = sign_up_in()
window2 = password()


timer = QTimer()
timer.timeout.connect(check)
timer.start(200)
     

window1.show()
app.exec()


# form,window = uic.loadUiType("password.ui")
# app = QApplication([])
# form = form()
# window = window()
# form.setupUi(window)
# window.setFixedSize(270,220)

# window.show()
# app.exec()
