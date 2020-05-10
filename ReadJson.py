import json

class ReadJson():
    def __init__(self, dir):
        with open(dir) as f:
            data = json.load(f)
        self.data = data
    def last_action(self):
        data = self.data
        last_action = data['transaction'][0]['action']
        return last_action

obj = ReadJson('logs/orders.json')
print (obj.last_action())
