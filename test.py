from PyQt6.QtWidgets import QApplication,QWidget,QLineEdit,QPushButton

app = QApplication([])

window = QWidget()
def text():
    app.exit()
    print(2)

line = QLineEdit(parent=window)
butten = QPushButton(parent=window)
butten.move(100,100)
butten.clicked.connect(text)

window.show()
app.exec()