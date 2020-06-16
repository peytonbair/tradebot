import json

class ReadJson():
    def __init__(self, dir):
        self.dir = dir
    def last_action(self):
        try:
            with open(self.dir) as f:
                data = json.load(f)
            last_action = data['transaction'][0]['action']
        except:
            last_action = 'sell'
        return last_action
    def last_price(self):
        try:
            with open(self.dir) as f:
                data = json.load(f)
            last_price = float(data['transaction'][0]['price']) #parse data and covert to float
        except:
            last_price = 0
        return last_price

obj = ReadJson('logs/orders.json')
print (obj.last_action())
