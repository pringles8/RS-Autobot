import os
import time

from dotenv import load_dotenv
import pyotp

load_dotenv()


def login(num_acct):
    import robin_stocks.robinhood as r

    totp = pyotp.TOTP(os.getenv("ROBINHOOD_TOTP").split(",")[num_acct].strip()).now()
    login = r.authentication.login(os.getenv("ROBINHOOD_USERNAME").split(",")[num_acct].strip(), \
                                   os.getenv("ROBINHOOD_PASSWORD").split(",")[num_acct].strip(), expiresIn=1800, \
                                   store_session=False, mfa_code=totp)

    return r


def robin_trade(buy=[], sell=[], acct=0):
    '''
    Robinhood - using robin_stocks but there is an api.
    Process: login -> get holdings -> buy stock if not already held.

    TO-DO:
    -
    '''

    r = login(acct)

    if len(buy) > 0:
        robin_buy(buy, r)
        print("Robin buying complete for user " + str(acct))
    if len(sell) > 0:
        robin_sell(sell, r)
        print("Robin selling complete for user " + str(acct))

    r.authentication.logout()
    print("Robin user " + str(acct) + " logout complete.")

    num_accts = len(os.getenv("ROBINHOOD_USERNAME").split(","))
    if acct + 1 != num_accts:
        robin_trade(buy, sell, acct=(acct + 1))


def robin_buy(stocks, r=None):
    holdings = r.build_holdings()
    holdings = holdings.keys()

    '''
    NOTES:
    Returns Dict indexed by ticker.
    {'CTXR': {'price': '1.110000', 'quantity': '11.08893400', 'average_buy_price': '1.2430', 'equity': '12.31', 'percent_change':
    '-10.70', 'equity_change': '-1.474828', 'type': 'stock', 'name': 'Citius Pharmaceuticals', 'id': '1be69e97-a90b-412b-8c49-5d1c
    66bca67a', 'pe_ratio': None, 'percentage': '3.04'}, 'PLTR': {'price': '7.380000', 'quantity': '1.81163800', 'average_buy_price
    ': '12.1859', 'equity': '13.37', 'percent_change': '-39.44', 'equity_change': '-8.706551', 'type': 'stock', 'name': 'Palantir
    Technologies', 'id': 'f90de184-4f73-4aad-9a5f-407858013eb1', 'pe_ratio': None, 'percentage': '3.30'},
    '''

    for stock in stocks:
        cash = float(r.profiles.load_account_profile()['buying_power'])

        if stock not in holdings and float(r.stocks.get_latest_price(stock, priceType='ask_price')[0] or cash) < cash:
            r.orders.order(stock, 1, 'buy',
                           limitPrice=float(r.stocks.get_latest_price(stock, priceType='ask_price')[0]),
                           timeInForce='gfd')

            time.sleep(1)
            holdings = r.build_holdings()
            holdings = holdings.keys()
            if stock in holdings:
                print('Bought ', stock, " in RH Brokerage")


def robin_sell(stocks, r=None):

    holdings = r.build_holdings()
    holdings = holdings.keys()

    '''
    NOTES:
    Returns Dict indexed by ticker.
    {'CTXR': {'price': '1.110000', 'quantity': '11.08893400', 'average_buy_price': '1.2430', 'equity': '12.31', 'percent_change':
    '-10.70', 'equity_change': '-1.474828', 'type': 'stock', 'name': 'Citius Pharmaceuticals', 'id': '1be69e97-a90b-412b-8c49-5d1c
    66bca67a', 'pe_ratio': None, 'percentage': '3.04'}, 'PLTR': {'price': '7.380000', 'quantity': '1.81163800', 'average_buy_price
    ': '12.1859', 'equity': '13.37', 'percent_change': '-39.44', 'equity_change': '-8.706551', 'type': 'stock', 'name': 'Palantir
    Technologies', 'id': 'f90de184-4f73-4aad-9a5f-407858013eb1', 'pe_ratio': None, 'percentage': '3.30'},
    '''
    for stock in stocks:
        if stock in holdings:
            r.orders.order(stock, 1, 'sell',
                           limitPrice=float(r.stocks.get_latest_price(stock, priceType='bid_price')[0]),
                           timeInForce='gfd')

            time.sleep(1)
            holdings = r.build_holdings()
            holdings = holdings.keys()
            if stock not in holdings:
                print('Sold ', stock, " in RH Brokerage")
