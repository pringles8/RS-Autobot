import os
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fidelity import fid_buy, fid_sell
from robhinhood import robin_buy, robin_sell


def first_buy(stocks):
    '''
    Firstrade - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    - Check if the holding stock already
    - Currently using last price but could use ask price or alert if large spread/dif between last and
        ask and give choice
    '''

    driver = uc.Chrome()
    driver.get("https://www.firstrade.com/content/en-us/welcome")
    wait = WebDriverWait(driver, 10)

    # Login
    element = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    element.send_keys(os.getenv("FIRSTRADE_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIRSTRADE_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
    element.click()
    return

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
    if val[1].strip().upper() == 'buy':
        buy.append(val[0].strip().upper())
    if val[1].strip().upper() == 'sell':
        sell.append(val[0].strip().upper())

    val = str(input("Enter another:\n"))

# Loop through the exchanges and pick brokers
##stocks = [i[1] for i in RS]

# Trade in brokers
stay_open = False
if len(buy) > 0 and len(sell) > 0:
    stay_open = True

    # API
    robin_buy(buy)
    obin_sell(sell)

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_buy(buy, stay_open, driver, wait)
    fid_sell(buy, stay_open, driver, wait)
    #first_buy(buy)
    #first_sell(buy)

    driver.quit()
elif len(buy) > 0:
    # API
    robin_buy(buy)

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 12)

    fid_buy(buy, stay_open, driver, wait)
    #first_buy(buy)

    driver.quit()
else:
    # API
    robin_sell(sell)

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_sell(sell, stay_open, driver, wat)
    #first_buy(buy)

    driver.quit()