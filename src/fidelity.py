import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

def open_website(driver, wait):
    driver.get("https://fidelity.com")
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "last-child")))
    element.click()
    return driver, wait

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fs-mask-username")))
    element.send_keys(os.getenv("FIDELITY_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIDELITY_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'fs-login-button')))
    element.click()

    # Click positions new-tab__tab
    element = wait.until(EC.element_to_be_clickable((By.ID, "portsum-tab-positions")))
    element.click()

    return

def log_out(wait):
    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "pntlt"]')))
    element = element.find_element(By.XPATH, '//a[@target = "_top"]')
    element.click()
    return

def get_positions(wait):
    # Get positions posweb-cell-symbol-name pvd-btn btn-anchor
    try:
        element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//button[@class = "posweb-cell-symbol-name pvd-btn btn-anchor"]')))
        if isinstance(element, list):
            positions = []
            for el in element:
                positions.append(el.text)
        else:
            positions = [element.text]
    except:
        positions = []

    return positions

def fid_buy(stocks, stay_open, driver, wait):
    '''
    Fidelity - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    - Check if holding stock already
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

    def fid_buy_modal(positions):
        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
        element.click()

        # Loop through stocks
        for s in stocks:
            if s not in positions:
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

    open_website(driver, wait)
    log_in(wait)
    time.sleep(1)

    # Get all accounts
    accounts = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "acct-selector__acct-title"]')))

    # Loop through accounts
    for account in accounts:
        time.sleep(1)
        account.click()
        positions = get_positions(wait)
        time.sleep(1)

        if not exclusions():
            fid_buy_modal(positions)

    print("Bought ", stocks, " in Fidelity")

    # Log out
    if not stay_open:
        log_out(wait)

def fid_sell(stocks, stay_open, driver, wait):
    '''
    Fidelity - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    - Check if holding stock already
    '''

    # Exclusions
    def exclusions():
        # exclude 401K accounts
        txt = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "portfolio-card-container__banner"]'))).text
        if "401K" in txt:
            return True
        else:
            return False

    def fid_sell_modal(positions):
        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
        element.click()

        # Loop through stocks
        for s in stocks:
            if s in positions:
                # Enter symbol
                element = wait.until(EC.element_to_be_clickable((By.ID, 'eq-ticket-dest-symbol')))
                element.send_keys(s)

                # Enter number of shares
                element = wait.until(EC.element_to_be_clickable((By.ID, 'eqt-shared-quantity')))
                element.send_keys(1)

                # Press buy, shares, day, and limit
                element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "pvd3-segment-root pvd-segment--medium"]')))
                for el in element:
                    if el.text == "Sell" or el.text == "Shares" or el.text == "Market" or el.text == "Day":
                        el.click()

                # Press preview and sell
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "eq-ticket__order-entry__actionbtn"]')))
                element.click()

                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "eq-ticket__order-entry__actionbtn"]')))
                element.click()

                # Close Modal
                element = wait.until(EC.element_to_be_clickable((By.XPATH,'//a[@class = "float-trade-container-close dialog-close"]')))
                element.click()

        return

    if not stay_open:
        open_website(driver, wait)
        log_in(wait)

    # Get all accounts
    accounts = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "acct-selector__acct-title"]')))

    # Loop through accounts
    for account in accounts:
        time.sleep(1)
        account.click()
        positions = get_positions(wait)
        time.sleep(1)

        if not exclusions():
            fid_sell_modal(positions)

    print("Sold ", stocks, " in Fidelity")

    log_out(wait)