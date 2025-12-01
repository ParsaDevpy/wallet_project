from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from function_class import main_app,sign_in,sign_up,forgot_password,intruduce,error,deposit_withdraw,chart
from models import Base
import os
charts = {}
def switch_window(win1,win2):
    win1.close()
    win2.show()
def open_window(win1):
    win1.show()
def open_chart(Currency):
    global charts
    if Currency not in charts:
        charts[Currency] = chart(Currency)
    charts[Currency].show()
    charts[Currency].raise_()

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
window6 = deposit_withdraw()
# chart_BTC = chart("bitcoin")
# chart_ETH = chart("ethereum")
# chart_USDT = chart("tether")



window5.show()


QTimer.singleShot(1100,lambda: switch_window(window5,window2))
      
window1.ETH_chart.connect(lambda: open_chart("ethereum"))
window1.BTC_chart.connect(lambda: open_chart("bitcoin"))
window1.USDT_chart.connect(lambda: open_chart("tether"))
window1.connect_error.connect(show_error)
window1.switch_window.connect(lambda: open_window(window6))
window2.sign_in_signal.connect(lambda: switch_window(window2,window1))
window2.sign_up_signal.connect(lambda: switch_window(window2,window3))
window2.password_signal.connect(lambda: switch_window(window2,window4))
window3.Email_available.connect(show_error)
window3.username_available.connect(show_error)
window3.fill_fields.connect(show_error)
window3.switch_main.connect(lambda: switch_window(window3,window2))
window4.verifi_error.connect(show_error)
window4.email_error.connect(show_error)
window4.switch_sign_in.connect(lambda: switch_window(window4,window2))


app.exec()

