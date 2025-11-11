import requests
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from time import sleep
from PyQt6.QtWidgets import QWidget,QApplication,QLabel

def nobitex(IRT):
    r = requests.get(f"https://apiv2.nobitex.ir/v3/orderbook/{IRT}IRT")
    data = r.json()

    if data["status"] == 'ok' :
        price = data['lastTradePrice']
        price = price[:-1]
        
    else:
        price = 404

    return price  


def update_price():
    form.label_4.setText(f'{nobitex("USDT")} تومان')
    form.label_5.setText(f'{nobitex("ETH")} تومان')
    form.label_6.setText(f'{nobitex("BTC")} تومان')
    if form.label_7.text() =='done!':
        form.label_7.setText("succesful!")
    elif form.label_7.text() == "" or "succesful!":
        form.label_7.setText("done!")

# def new_window():
   
#     window2 = QWidget()
 
#     label = QLabel("coming soon.....",parent=window2)

#     window2.show()
    


Form, Window = uic.loadUiType("wallet.ui")
app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.setFixedSize(241,170)

form.label_4.setText(f'{nobitex("USDT")} تومان')
form.label_5.setText(f'{nobitex("ETH")} تومان')
form.label_6.setText(f'{nobitex("BTC")} تومان')
form.pushButton_5.clicked.connect(update_price)
form.comboBox.addItems(['BTCIRT','ETHIRT','USDTIRT'])
# for i in range(1,5):
#     butten = getattr(form,f'pushButton_{i}')
#     butten.clicked.connect(new_window)


window.show()
app.exec()


