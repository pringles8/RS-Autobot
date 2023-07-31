import json

#uri's
cert_url='https://api.cert.tastyworks.com'
prod_url='https://api.tastyworks.com'

import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Login
def login(acct):
    url = prod_url+"/sessions"
    body = {
        "login": os.getenv("TASTYTRADE_USERNAME").split(",")[acct].strip(),
        "password": os.getenv("TASTYTRADE_PASSWORD").split(",")[acct].strip(),
        "remeber-me": False
    }
    response = requests.post(url=url, data=body)
    response = response.json()
    session_token = response["data"]["session-token"]

    return session_token

# Logout
def logout(session_token):
    url = prod_url+"/sessions"
    response = requests.delete(url=url, headers={"Authorization": session_token})
    if response.status_code == 204:
        print("Tasty Logout Complete")

def order(stock, acct_num, st, side):
    url = prod_url + "/accounts/{}/orders".format(acct_num)
    headers = {"Authorization": st, "Content-Type": "application/json"}

    if side == "Buy":
        action = "Buy to Open"
        priceEffect = "Debit"
    else:
        action = "Sell to Close"
        priceEffect = "Credit"
    legs = [{"instrument-type": "Equity", "symbol": stock, "quantity": 1, "action": action}]
    body = {
        "time-in-force": "Day",
        "order-type": "Market",
        "price-effect": priceEffect,
        "legs": legs
    }

    response = requests.post(url=url, headers=headers, data=json.dumps(body))

    if response.status_code == 201:
        buysell = "Bought " if side == "Buy" else "Sold "
        print(buysell + stock + " in Tasty account " + acct_num[-4:])
    else:
        response = response.json()
        print(response)


def TastyTrade(buy, sell, acct=0):
    # Get accounts
    st = login(acct)

    # Get accounts
    url = prod_url+"/customers/me/accounts"
    headers={"Authorization": st}
    response = requests.get(url=url, headers=headers)
    response = response.json()
    #["data"]["items"] is then a list of dicts
    accts = response["data"]["items"]

    # Loop through accounts:
    for act in accts:
        acct_num = act['account']["account-number"]

        # Get positions
        url = prod_url + "/accounts/{}/positions".format(acct_num)
        headers = {"Authorization": st}
        response = requests.get(url=url, headers=headers)
        response = response.json()
        positions = response["data"]["items"]
        positions = [p["symbol"] for p in positions]

        # Get balances
        url = prod_url + "/accounts/{}/balances".format(acct_num)
        headers = {"Authorization": st}
        response = requests.get(url=url, headers=headers)
        response = response.json()
        balances = response["data"] # We want cash-balance

        # Put in orders
        if len(buy) > 0:
            for stock in buy:
                if stock not in positions:
                    order(stock=stock, acct_num=acct_num, st=st, side="Buy")
            print("Tasty buying complete for account " + str(acct_num)[-4:])
        if len(sell) > 0:
            for stock in sell:
                if stock in positions:
                    order(stock=stock, acct_num=acct_num, st=st, side="Sell")
            print("Tasty selling complete for account " + str(acct_num)[-4:])

    logout(st)
    print("Tasty totally complete for acount " + str(acct_num)[-4:])

    num_accts = len(os.getenv("TASTYTRADE_USERNAME").split(","))
    if acct + 1 != num_accts:
        TastyTrade(buy, sell, acct=(acct + 1))