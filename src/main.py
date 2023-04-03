import os
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fidelity import fid_buy, fid_sell
from robhinhood import robin_buy, robin_sell
#from firstrade import first_buy

# Main
'''
TO-DO:
- After-hours capabillity
- Add quantity and other defaults into env
- Add more brokers
- Vet by exchange/broker pair
- Exclusions for brokerage, accounts, etc.
- Track and sell
'''

load_dotenv()

# Get inputs
buy = []
sell = []
#buy = ['O'] # For testing purposes
#sell = ['O'] # For testing purposes

# Take inputs

print("Enter stock ticker and side of order i.e. 'vti,buy'\nTo end input, enter 'done': ")
val = str(input())
while 1 == 1:
    if val.strip().lower() == 'done':
        break

    val = val.split(',')
    if val[1].strip().lower() == 'buy':
        buy.append(val[0].strip().upper())
    if val[1].strip().lower() == 'sell':
        sell.append(val[0].strip().upper())

    val = str(input("Enter another:\n"))

# Loop through the exchanges and pick brokers
##stocks = [i[1] for i in RS]

# Trade in brokers
stay_open = False
if len(buy) > 0 and len(sell) > 0:
    stay_open = True

    # API
    import robin_stocks.robinhood as r
    login = r.authentication.login(os.getenv("ROBINHOOD_USERNAME"), os.getenv("ROBINHOOD_PASSWORD"))

    robin_buy(buy, r)
    robin_sell(sell, r)

    r.authentication.logout()

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_buy(buy, stay_open, driver, wait)
    fid_sell(buy, stay_open, driver, wait)
    #first_buy(buy, stay_open, driver, wait)
    #first_sell(sell, stay_open, driver, wait)

    driver.quit()
elif len(buy) > 0:
    # API
    robin_buy(buy)

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 12)

    fid_buy(buy, stay_open, driver, wait)
    #first_buy(buy, stay_open, driver, wait)

    driver.quit()
else:
    # API
    robin_sell(sell)

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_sell(sell, stay_open, driver, wait)
    #first_sell(sell, stay_open, driver, wait)

    driver.quit()