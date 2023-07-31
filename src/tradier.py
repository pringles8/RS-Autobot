import json
import os

#uri's
url='https://api.tradier.com/v1/'

import requests
import os
from dotenv import load_dotenv

load_dotenv()

def order(stock, acc_num, header, side):
    response = requests.post(url+'accounts/{}/orders'.format(acc_num),
                             data={'class': 'equity', 'symbol': stock, 'side': side, 'quantity': '1',
                                   'type': 'market', 'duration': 'day', 'price': '1.00', 'stop': '1.00',
                                   'tag': 'my-tag-example-1'},
                             headers=header
                             )
    json_response = response.json()
    print(response.status_code)
    if response.status_code == "200":
        print(side + ' ' + stock + ' in ' + acc_num[-4] + ' done.')
def tradierTrade(buy, sell, acct=0):
    # Get Accounts
    headers={'Authorization': 'Bearer '+ os.getenv("TRADIER_ACCESS_TOKEN"), 'Accept': 'application/json'}

    response = requests.get(url + 'user/profile',
        params={},
        headers=headers
    )

    json_response = response.json()
    json_response = json_response['profile']["account"]

    # Loop through accounts
    for account in json_response:
        acc_num = account['account_number']

        # Get positions
        response = requests.get(url+'accounts/{}/positions'.format(acc_num),
                                params={},
                                headers=headers
        )

        json_response = response.json()
        json_response = json_response['positions']
        if json_response == 'null':
            positions = []
        else:
            json_response = json_response['position']
            positions = [i['symbol'] for i in json_response]

        # Make trades
        if len(buy) > 0:
            for stock in buy:
                if stock not in positions:
                    order(stock=stock, acc_num=acc_num, header=headers, side="buy")
        if len(sell) > 0:
            for stock in sell:
                if stock in positions:
                    order(stock=stock, acc_num=acc_num, header=headers, side="sell")