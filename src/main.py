def fid_buy(stock):
    driver.get("https://fidelity.com")
    wait = WebDriverWait(driver, 12)
    element = driver.find_element(By.CLASS_NAME, "last-child")
    element.click()
    wait = WebDriverWait(driver, 12)

    # Login
    element = driver.find_element(By.CLASS_NAME, "fs-mask-username")
    element.send_keys("pringleshelat")
    wait = WebDriverWait(driver, 2)
    element = driver.find_element(By.ID, 'password')
    element.send_keys("Hanuman.1")
    wait = WebDriverWait(driver, 2)
    element = driver.find_element(By.ID, 'fs-login-button')
    element.click()
    wait = WebDriverWait(driver, 12)

    # Open Trade Modal
    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
    except StaleElementReferenceException:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))

    element.click()
    wait = WebDriverWait(driver, 2)

    element = driver.find_element(By.ID, "dest-acct-dropdown")
    element.click()

    try:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ett-acct-sel-list")))
    except NoSuchElementException:
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "ett-acct-sel-list")))

    #element = driver.find_element(By.CLASS_NAME, "ett-acct-sel-list")
    #print(element.size)
    # ['Individual - TOD (Z09446147)', 'ROTH IRA (233798797)', 'Traditional IRA (238697913)', 'Fidelity Bloom ℠ Sp...(*5583)', 'Fidelity Bloom ℠ Save (*1860)']
    # Class name = ett-acct-sel-list
    #Accounts = Select(element)
    #print(Accounts.Options())

    #element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
    #element.click()
    #wait = WebDriverWait(driver, 1)
    #element = driver.find_element(By.ID, "dest-acct-dropdown")
    #Accounts = Select(element)
    #print(Accounts.Options())


def robin_buy(stock):
    '''
    Robinhood - using robin_stocks but there is an api.
    Process: login -> get holdings -> buy stock if not already held.
    '''
    import robin_stocks.robinhood as r
    #import robin_stocks.robinhood as rs_login

    login = r.authentication.login('pringleshelat@gmail.com','DicksOut4Stonk')

    holdings = r.build_holdings()
    holdings = holdings.keys()
    '''
    Returns Dict indexed by ticker.
    {'CTXR': {'price': '1.110000', 'quantity': '11.08893400', 'average_buy_price': '1.2430', 'equity': '12.31', 'percent_change':
    '-10.70', 'equity_change': '-1.474828', 'type': 'stock', 'name': 'Citius Pharmaceuticals', 'id': '1be69e97-a90b-412b-8c49-5d1c
    66bca67a', 'pe_ratio': None, 'percentage': '3.04'}, 'PLTR': {'price': '7.380000', 'quantity': '1.81163800', 'average_buy_price
    ': '12.1859', 'equity': '13.37', 'percent_change': '-39.44', 'equity_change': '-8.706551', 'type': 'stock', 'name': 'Palantir
    Technologies', 'id': 'f90de184-4f73-4aad-9a5f-407858013eb1', 'pe_ratio': None, 'percentage': '3.30'},
    '''
    cash = r.profiles.load_account_profile()['buying_power']

    if stock[0] not in holdings and r.stocks.get_latest_price(stock[0], priceType = 'ask_price') < cash:
        r.orders.order(stock[0], 1, 'buy', limitPrice = r.stocks.get_latest_price(stock[0], priceType = 'ask_price'), timeInForce = 'gfd')

    holdings = r.build_holdings()
    holdings = holdings.keys()
    if stock[0] in holdings:
        print('Bought:', stock[0])

    r.authentication.logout()

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

# Set up selenium
#options = webdriver.ChromeOptions()
#options.add_argument('headless')

driver = uc.Chrome()

# Get inputs
accounts = {}
RS = set()
'''
print("Enter stock ticker and exchange i.e. 'VTI,Nasdaq'\nTo end input, enter 'done': ")
val = str(input())
while 1 == 1:
    if val.strip().lower() == 'done':
        break
    val = val.split(',')
    RS.add((val[0].strip().upper(), val[1].strip().upper()))
    val = str(input("Enter another:\n"))
'''
# Loop through the exchanges and pick brokers
##stocks = [i[1] for i in RS]

# Trade in brokers
RS = {('O', 'NYSE')} # For testing purposes
for stock in RS:

    fid_buy(stock)
    # robin_buy(stock)
