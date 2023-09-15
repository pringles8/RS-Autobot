import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

def open_website(driver):
    driver.get("https://client.schwab.com/Login/SignOn/CustomerCenterLogin.aspx")
    #time.sleep(3)
    return

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="sdps-form-element__control"]')))
    element.send_keys(os.getenv("SCHWAB_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="sdps-form-element__control"]')))
    element.send_keys(os.getenv("SCHWAB_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'btnLogin')))
    element.click()
    return

def log_out(wait):
    # Logout
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="logout btn btn-clear-blue"]')))
    try:
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Log Out')))
    except:
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Log Out')))

    element.click()
    print('Scwab Logout Complete.')
    return

def get_positions(wait):
    # Click positions
    positions = []

def schwab_buy_and_sell(driver, wait, buy=[], sell=[], acct=0):
    '''
    Schwab - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    '''

    def exclusions():
        return

    def schwab_ticket(side):
        # Input ticker
        element = wait.until(EC.element_to_be_clickable((By.ID, '_txtSymbol')))
        element.send_keys(s)

        if side == "Buy":
            # Chose side of trade
            element = wait.until(EC.element_to_be_clickable((By.ID, '_action')))
            element.click()

            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//option[@value="49"]')))  # 49 for buy and 50 for sell
            element.click()

            # Get ask price and input limit price
            lim_price = wait.until(EC.element_to_be_clickable((By.ID, 'mcaio-asklink')))
            lim_price = lim_price.text

            element = wait.until(EC.element_to_be_clickable((By.ID, 'limitprice-stepper-input')))
            element.send_keys(lim_price)
        else:
            # Press sell all
            try:
                sell_all = wait.until(EC.element_to_be_clickable((By.ID, 'mcaio-sellAllHandle')))
            except:
                return

            if sell_all is not None:
                sell_all.click()

        # Press review button
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="mcaio-order--reviewbtn sdps-button sdps-button--primary"]')))
        element.click()

        # Press place order button
        element = wait.until(EC.element_to_be_clickable((By.ID, 'mtt-place-button')))
        element.click()

        print(side + " " + s + " in account " + el.text[:-4] + "complete." )

        # Press place another order button -
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="sdps-button sdps-button--secondary mcaio--mcaio-cta-buttons-anothertrade"]')))
        element.click()

        return

    open_website(driver)
    log_in(wait)

    # Go to trade tab and ticket
    element = wait.until(EC.element_to_be_clickable((By.ID, 'meganav-button-trade')))
    element.click()

    element = wait.until(EC.element_to_be_clickable((By.ID, 'meganav-secondary-menu-aio')))
    element.click()

    # Loop through accounts
    element = wait.until(EC.element_to_be_clickable((By.ID, 'mcAccountSelector')))
    element.click()

    element = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'sdps-account-selector__list-item')))

    for el in element:
        el.click()

        # Make trade
        if len(buy) > 0:
            for s in buy:
                schwab_ticket("Buy")
        if len(sell) > 0:
            for s in sell:
                schwab_ticket("Sell")

        element = wait.until(EC.element_to_be_clickable((By.ID, 'mcAccountSelector')))
        element.click()

    log_out(wait)
    return