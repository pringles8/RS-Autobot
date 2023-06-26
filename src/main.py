import os
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

from fidelity import fid_buy_and_sell
from robhinhood import robin_buy, robin_sell
from firstrade import first_buy_and_sell

# Main
'''
TO-DO:
- After-hours capabillity
- Add quantity and other defaults into env
- Add more brokers
- Vet by exchange/broker pair
- appium for mobile apps  6
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

print("\nEnter side of order and stock ticker(s) i.e. 'buy, vti, qqq'\nTo end input, enter 'done': ")
val = str(input())
while 1 == 1:
    if val.strip().lower() == 'done':
        print()
        break

    val = list(map(str.strip, val.split(',')))

    if val[0].lower() == 'buy':
        buy = buy + list(map(str.upper, val[1:]))
        buy = [*set(buy)] # Dedup
    elif val[0].lower() == 'sell':
        sell = sell + list(map(str.upper, val[1:]))
        sell = [*set(sell)]

    else:
        val = str(input("Please input a valid order.\n Try again:\n"))
        continue

    val = str(input("Enter more:\n"))

# Loop through the exchanges and pick brokers
##stocks = [i[1] for i in RS]

# Trade in brokers

stay_open = False
if len(buy) > 0 and len(sell) > 0:
    stay_open = True

    # API
    import robin_stocks.robinhood as r
    import pyotp

    for num_accounts in range(len(os.getenv('ROBINHOOD_USERNAME').split(","))):
        totp = pyotp.TOTP(os.getenv("ROBINHOOD_TOTP").split(",")[num_accounts].strip()).now()
        login = r.authentication.login(os.getenv("ROBINHOOD_USERNAME").split(",")[num_accounts].strip(), os.getenv("ROBINHOOD_PASSWORD").split(",")[num_accounts].strip(), expiresIn=1800, store_session=False, mfa_code=totp)

        robin_buy(buy, stay_open, r)
        print("RH Buying Complete.")
        robin_sell(sell, stay_open, r)
        print("RH Selling Complete.")

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_buy_and_sell(buy, stay_open, driver, wait, side='Buy')
    print("Fid Buying Complete.")
    fid_buy_and_sell(sell, stay_open, driver, wait, side='Sell')
    print("Fid Selling Complete.")
    first_buy_and_sell(buy, stay_open, driver, wait, side='Buy')
    print("First Buying Complete.")
    first_buy_and_sell(buy, stay_open, driver, wait, side='Sell')
    print("First Selling Complete.")

    driver.quit()
    print("Driver Quit Complete.")

elif len(buy) > 0:
    # API
    robin_buy(buy, stay_open)
    print("RH Buying Complete.")

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_buy_and_sell(buy, stay_open, driver, wait, side='Buy')
    print("Fid Buying Complete.")
    first_buy_and_sell(buy, stay_open, driver, wait, side="Buy")
    print("First Buying Complete.")

    driver.quit()
    print("Driver Quit Complete.")
else:
    # API
    #robin_sell(sell, stay_open)
    print("RH Selling Complete.")

    # Selenium
    driver = uc.Chrome()
    wait = WebDriverWait(driver, 10)

    fid_buy_and_sell(sell, stay_open, driver, wait, side='Sell')
    print("Fid Selling Complete.")
    first_buy_and_sell(sell, stay_open, driver, wait, side='Sell')
    print("First Selling Complete.")

    driver.quit()
    print("Driver Quit Complete.")
