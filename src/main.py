from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import os
from dotenv import load_dotenv
from dotenv import dotenv_values
def fid_buy(stocks):
    '''
    Fidelity - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    - Check if the holding stock already
    - Currently using last price but could use ask price or alert if large spread/dif between last and
        ask and give choice
    '''

    # Exclusions
    def exclusions():
        # exclude 401K accounts
        txt = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "portfolio-card-container__banner"]'))).text
        if "401K" in txt:
            return True
        else:
            return False

    def fid_buy_modal():
        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
        element.click()

        # Loop through stocks
        for s in stocks:
            # Enter symbol
            element = wait.until(EC.element_to_be_clickable((By.ID, 'eq-ticket-dest-symbol')))
            element.send_keys(s)

            # Enter number of shares
            element = wait.until(EC.element_to_be_clickable((By.ID, 'eqt-shared-quantity')))
            element.send_keys(1)

            # Press buy, shares, day, and limit
            element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "pvd3-segment-root pvd-segment--medium"]')))
            for el in element:
                if el.text == "Buy" or el.text == "Shares" or el.text == "Limit" or el.text == "Day":
                    el.click()

            # Input last price
            last_price = wait.until(EC.element_to_be_clickable((By.ID, 'eq-ticket__last-price'))).text

            element = wait.until(EC.element_to_be_clickable((By.ID, 'eqt-ordsel-limit-price-field')))
            element.send_keys(last_price)

            # Press preview and buy
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "eq-ticket__order-entry__actionbtn"]')))
            element.click()

            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "eq-ticket__order-entry__actionbtn"]')))
            element.click()

            # Close Modal
            element = wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class = "float-trade-container-close dialog-close"]')))
            element.click()

        return

    driver = uc.Chrome()
    driver.get("https://fidelity.com")
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "last-child")))
    element.click()

    # Login
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fs-mask-username")))
    element.send_keys(os.getenv("FIDELITY_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIDELITY_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'fs-login-button')))
    element.click()

    # Get all accounts
    accounts = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "acct-selector__acct-title"]')))

    # Loop through accounts
    for account in accounts:
        account.click()

        if not exclusions():
            fid_buy_modal()

    print("Bought ", RS, " in Fidelity")

    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "pntlt"]')))
    element = element.find_element(By.XPATH, '//a[@target = "_top"]')
    element.click()

    # Close
    driver.quit()
def robin_buy(stock):
    '''
    Robinhood - using robin_stocks but there is an api.
    Process: login -> get holdings -> buy stock if not already held.

    TO-DO:
    -
    '''

    import robin_stocks.robinhood as r

    login = r.authentication.login(os.getenv("ROBINHOOD_USERNAME"), os.getenv("ROBINHOOD_PASSWORD"))

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

    cash = float(r.profiles.load_account_profile()['buying_power'])

    if stock not in holdings and float(r.stocks.get_latest_price(stock, priceType = 'ask_price')[0]) < cash:
        r.orders.order(stock, 1, 'buy', limitPrice = float(r.stocks.get_latest_price(stock, priceType = 'ask_price')[0]), timeInForce = 'gfd')

    holdings = r.build_holdings()
    holdings = holdings.keys()
    if stock in holdings:
        print('Bought ', stock, " in RH Brokerage")

    r.authentication.logout()

# Main
'''
TO-DO:
- Add more brokers
- Vet by exchange/broker pair
- Exclusions for brokerage, accounts, etc.
- Track and sell
'''
load_dotenv()

# Get inputs
RS = {}

# Take inputs
print("Enter stock ticker and exchange i.e. 'VTI,Nasdaq'\nTo end input, enter 'done': ")
val = str(input())
while 1 == 1:
    if val.strip().lower() == 'done':
        break
    val = val.split(',')
    RS[val[0].strip().upper()] = val[1].strip().upper()
    val = str(input("Enter another:\n"))

# Loop through the exchanges and pick brokers
##stocks = [i[1] for i in RS]

# Trade in brokers
#RS = {'O':'NYSE'} # For testing purposes

for stock in RS.keys():
    robin_buy(stock)

fid_buy(RS.keys())
