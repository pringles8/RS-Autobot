import os
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

from fidelity import fid_buy_and_sell
from robhinhood import robin_trade
from firstrade import first_buy_and_sell
from tastytrade import TastyTrade
from tradier import tradierTrade

# Main
'''
TO-DO:
- After-hours capability
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

print("\nEnter side of order and stock ticker(s). To end input, enter 'done'.\ni.e. 'buy, vti, qqq' or 'sell, voo, q, "
      "done' or 'done'.")
val = str(input())
while 1 == 1:
    if val.strip().lower() == 'done':
        print()
        break

    val = list(map(str.strip, val.split(',')))
    if val[-1].strip().lower() == 'done':
        bre = True
        val.pop()
    else:
        bre = False

    if val[0].lower() == 'buy':
        buy = buy + list(map(str.upper, val[1:]))
        buy = [*set(buy)]  # Dedup
    elif val[0].lower() == 'sell':
        sell = sell + list(map(str.upper, val[1:]))
        sell = [*set(sell)]
    else:
        val = str(input("Please input a valid order.\n Try again:\n"))
        continue

    if bre:
        break

    val = str(input("Enter more:\n"))

# Loop through the exchanges and pick brokers
##stocks = [i[1] for i in RS]

# Trade in brokers
## API First
robin_trade(buy=buy, sell=sell)
print("Robinhood orders complete. ------------------------------------")

TastyTrade(buy=buy, sell=sell)
print("Tasty orders complete. ------------------------------------")

tradierTrade(buy=buy, sell=sell)
print("Tradier orders complete. ------------------------------------")

## Browser/Selenium Crawling
driver = uc.Chrome()
wait = WebDriverWait(driver, 10)

### Fidelity
fid_buy_and_sell(driver=driver, wait=wait, buy=buy, sell=sell)
print("Fidelity orders complete. ------------------------------------")

### Firstrade
first_buy_and_sell(driver=driver, wait=wait, buy=buy, sell=sell)
print("Firstrade orders complete. ------------------------------------")

driver.quit()
print("Driver Quit Complete.")
