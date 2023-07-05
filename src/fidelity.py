import time
import os
from dotenv import load_dotenv
import math
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()

def open_website(driver, wait):
    driver.get("https://fidelity.com")
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "last-child")))
    element.click()

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fs-mask-username")))
    element.send_keys(os.getenv("FIDELITY_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIDELITY_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'fs-login-button')))
    element.click()
    time.sleep(10)

    # Click positions
    element = wait.until(EC.visibility_of_element_located((By.ID, "portsum-tab-positions")))
    element.click()
    time.sleep(10)

    # Wait for refresh
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//button[@class = "posweb-cell-symbol-name pvd-btn btn-anchor"]')))

    return

def log_out(wait):
    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "pntlt"]')))
    element = element.find_element(By.XPATH, '//a[@target = "_top"]')
    element.click()
    print("Fid Logout Complete.")
    return

def get_positions(wait):
    # Get positions
    try:
        element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//button[@class = "posweb-cell-symbol-name pvd-btn btn-anchor"]')))
        if isinstance(element, list):
            positions = [el.text for el in element]
        else:
            positions = [element.text]
    except:
        positions = []

    return positions

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def fid_buy_and_sell(driver, wait, buy=[], sell=[]):
    '''
    Fidelity - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    - Check all positions and remove tickers from list/skip step after checking
    - Currently using last price but could use ask price or alert if large spread/dif between last and
        ask and give choice
    '''

    # Exclusions
    def exclusions():
        # exclude non-self-directed accounts
        txt = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "portfolio-card-container__banner"]'))).text
        if any(item in txt for item in ["401K", "CHET", "529"]):
            return True
        else:
            return False

    def fid_modal(side):
        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
        element.click()

        # Enter symbol
        wait.until(EC.visibility_of_element_located((By.ID, 'eq-ticket-dest-symbol')))
        element = wait.until(EC.element_to_be_clickable((By.ID, 'eq-ticket-dest-symbol')))
        element.send_keys(stock)

        # Enter number of shares
        element = wait.until(EC.element_to_be_clickable((By.ID, 'eqt-shared-quantity')))
        element.send_keys(1)

        market_or_limit = 'Market' if side == 'Sell' else "Limit"

        # Press buy, shares, day, and limit
        element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "pvd3-segment-root pvd-segment--medium"]'))) #//label[@class = "pvd-segment__label"]

        for el in element:
            if el.text == side or el.text == "Shares" or el.text == market_or_limit or el.text == "Day" or el.text == "Cash":
                time.sleep(1)
                ActionChains(driver).move_to_element(el).click(el).perform()

        if side == "Buy":
            # Input last price
            #last_price = wait.until(EC.element_to_be_clickable((By.ID, 'eq-ticket__last-price'))).text

            # Input ask price
            ask_price = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="block-price-layout"]')))
            ask_price = round_up(float(ask_price[1].text.split("x")[0].strip()), 2)

            element = wait.until(EC.element_to_be_clickable((By.ID, 'eqt-ordsel-limit-price-field')))
            element.send_keys(ask_price)

        # Press preview and buy
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "eq-ticket__order-entry__actionbtn"]')))
        element.click()

        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "eq-ticket__order-entry__actionbtn"]')))
        element.click()

        # Wait to process/last modal screen
        wait.until(EC.element_to_be_clickable((By.ID, 'Enter_order_button'))) # Time out errors here

        # Close Modal
        element = wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class = "float-trade-container-close dialog-close"]')))
        element.click()

        return
    # Open and login
    open_website(driver, wait)
    log_in(wait)

    # Get all accounts
    accounts = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="acct-selector__acct-content"]')))

    # Loop through accounts
    for i in range(len(accounts)):
        account = accounts[i]

        if EC.staleness_of(account):
            accounts = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="acct-selector__acct-content"]')))
            account = accounts[i]

        ActionChains(driver).move_to_element(account).click(account).perform()

        if not exclusions():
            positions = get_positions(wait)

            # Loop through stocks
            if len(buy) > 0:
                for stock in buy:
                    if stock not in positions:
                        fid_modal(side="Buy")
                        print('Bought ', stock, " in Fid account " + str(account.text))
                    time.sleep(1)
                print("Fid buying complete in account " + str(account.text))
            if len(sell) > 0:
                for stock in sell:
                    if stock in positions:
                        fid_modal(side="Sell")
                        print('Sold ', stock, " in Fid account " + str(account.text))
                    time.sleep(1)
                print("Fid selling complete in account " + str(account.text))
        else:
            wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//button[@class = "posweb-cell-symbol-name pvd-btn btn-anchor"]')))

    log_out(wait)

    return
