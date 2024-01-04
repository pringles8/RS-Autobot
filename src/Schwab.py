import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

load_dotenv()

def open_website(driver):
    driver.get("https://client.schwab.com/Login/SignOn/CustomerCenterLogin.aspx")
    time.sleep(3)
    return

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.ID, 'loginIdInput')))
    element.send_keys(os.getenv("SCHWAB_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'passwordInput')))
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
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="_txtSymbol"]')))
        element.clear()
        element.send_keys(s)
        time.sleep(2)
        element.send_keys(Keys.TAB)
        time.sleep(2)

        if side == "Buy":
            # Check if owned
            try:
                element = wait.until(EC.visibility_of_element_located((By.ID, 'mcaio-sellAllHandle')))
            except:
                element = None

            if element is not None:
                return

            # Chose side of trade
            element = wait.until(EC.element_to_be_clickable((By.ID, '_action')))
            element.click()

            element = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//option[@value="49"]')))  # 49 for buy and 50 for sell
            element.click()

            # Get ask price and input limit price
            ask_price = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class,"askLink ")]')))
            ask_price.click()

        else:
            # Press sell all
            try:
                sell_all = wait.until(EC.element_to_be_clickable((By.ID, 'mcaio-sellAllHandle')))
            except:
                return

            if sell_all is not None:
                sell_all.click()

                lim_price = wait.until(EC.element_to_be_clickable((By.ID, 'mcaio-bidlink')))
                lim_price.click()

        # Press review button
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="mcaio-order--reviewbtn sdps-button sdps-button--primary"]')))
        element.click()

        # Press place order button
        element = wait.until(EC.element_to_be_clickable((By.ID, 'mtt-place-button')))
        element.click()

        print(side + " " + s + " in account " + acc_text + "complete." )

        # Press place another order button -
        element = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@class="sdps-button sdps-button--secondary mcaio--mcaio-cta-buttons-anothertrade"]')))
        element.click()

        return

    open_website(driver)
    driver.switch_to.frame(driver.find_element(By.ID, 'lmsSecondaryLogin'))
    log_in(wait)
    driver.switch_to.default_content()

    # Go to trade tab and ticket
    time.sleep(1)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="footer-aio"]')))
    element.click()
    time.sleep(3)

    # Loop through accounts
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="basic-example-small"]')))
    element.click()
    time.sleep(3)

    element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//li[@class="sdps-account-selector__list-item"]')))

    for i in range(len(element)):
        element[i].click()
        acc_text = element[i].text[:-4]
        time.sleep(3)

        # Make trade
        if len(buy) > 0:
            for s in buy:
                schwab_ticket("Buy")
        if len(sell) > 0:
            for s in sell:
                schwab_ticket("Sell")

        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@id="basic-example-small"]')))
        element.click()
        time.sleep(2)

        element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//li[@class="sdps-account-selector__list-item"]')))


    log_out(wait)
    return