from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from threading import Thread
from function_class import main_app,sign_up_in
import json
# global switch
# switch = False
# def check(check):
#     while True:
#         if check == "sign_up":
#             global switch
#             switch = True
#         if switch:
#             window1.close()
#             window2.show()
         
# app = QApplication([])

# window1 = sign_up_in()
# window2 = main_app()
# check_Thread = Thread(target=check)
# check_Thread.start()

     
# with open("word.json","r") as f:
#     check_json = json.load(f)["check"]

# window1.show()
# app.exec()
app = QApplication([])

window1 = sign_up_in()

window1.show()
app.exec()