from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from threading import Thread
from function_class import main_app,sign_up_in
import json

o = sign_up_in([])
with open("word.json","r") as f:
    if json.load(f)["check"] == "sign_up":
        check = True
if check:
    o1 = main_app([])
