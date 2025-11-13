import requests

def nobitex(IRT):
    r = requests.get(f"https://apiv2.nobitex.ir/v3/orderbook/{IRT}IRT")
    data = r.json()

    if data["status"] == 'ok' :
        price = data['lastTradePrice']
        price = price[:-1]
        
    else:
        price = 404

    return price 


