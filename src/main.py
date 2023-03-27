import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

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
if len(buy) > 0:
    robin_buy(buy)
    fid_buy(buy)
    #first_buy(buy)

if len(sell) > 0:
    #robin_sell(sell)
    #fid_sell(sell)
