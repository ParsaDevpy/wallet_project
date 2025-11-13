from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from threading import Thread
from function_class import main_app


Form, Window = uic.loadUiType("sign up_in.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.setFixedSize(241,205)





window.show()
app.exec()



