import json


class OrderLog:
    def __init__(self):
        pass

    def record(self, pair, action, time, price):
        with open('logs/orders.json', 'a+') as file:
            try:
                details = json.load(file)
            except:
                details = {}
                details['transaction'] = []


            details['transaction'].insert(0,{
                'name': pair,
                'action': action,
                'time': time,
                'price': price,
                'balance': 0
            })
            file.truncate(0)
            file.write(json.dumps(details, indent=4, sort_keys=True))


    def get_record(self):
        with open('record.json', 'r') as file:

            try:
                data = json.load(file)
                last_time = data['transaction'][0]['time']
                last_action = data['transaction'][0]['action']
                last_price = data['transaction'][0]['price']

            except:

                last_action = 'sell'
                last_price = 0
