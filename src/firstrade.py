import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

def open_website(driver, wait):
    driver.get("https://www.firstrade.com/content/en-us/welcome")
    return

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    element.send_keys(os.getenv("FIRSTRADE_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIRSTRADE_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
    element.click()
    return

def log_out(wait):
    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="logout btn btn-clear-blue"]')))
    element.click()
    print('First Logout Complete.')
    return

def get_positions(wait):
    # Click positions
    try:
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn-white"]')))
        element.click()

        element = wait.until(EC.visibility_of_element_located((By.ID, 'pos_view0')))
        element = element.find_elements((By.XPATH, '//td[@class="ta_left"]'))

        if isinstance(element, list):
            positions = [el.text for el in element]
        else:
            positions = [element.text]
    except:
        positions = []

    return positions

def first_buy_and_sell(stocks, stay_open, driver, wait, side):
    '''
    Firstrade - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    - Currently using last price but could use ask price or alert if large spread/dif between last and
        ask and give choice
    '''

    def exclusions():
        return

    def first_modal(side):
        # Press buy radio button
        buy_sell_xpath = "transactionType_Buy" if side == "Buy" else "transactionType_Sell"
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="{}"]'.format(buy_sell_xpath))))
        element.click()

        # Enter quantity
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quantity"]')))
        element.send_keys(1)

        # Enter ticker and limit prices
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quoteSymbol"]')))
        element.send_keys(s)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="getQ"]')))
        element.click()

        # Send order
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="submitOrder"]')))
        element.click()

        # Place another order
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="submitted_placeorder_bnt btn btn-action"]')))
        element.click()
        return

    if (not stay_open) or (stay_open and side == 'Buy'):
        open_website(driver, wait)
        log_in(wait)
        time.sleep(3)

    # Check for PIN //div[@class="subtitle"]
    if driver.current_url == "https://invest.firstrade.com/cgi-bin/enter_pin":
        for i in os.getenv('FIRSTRADE_PIN'):
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title={}]".format(i))))
            element.click()

        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="submit"]')))
        element.click()

    # Get all accounts
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'change_acon')))
    element.click()
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="change_acon_db"]')))
    element = element.find_elements(By.XPATH, '//a[@href="javascript:void(0)"]')
    print(len(element))

    # Loop through accounts and buy
    for el in element:
        el.click()

        positions = get_positions(wait)

        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="javascript:ChangeOrderbar();"]')))
        element.click()

        # Loop through stocks
        for s in stocks:
            if side == "Buy":
                if s not in positions:
                    first_modal(side)
            else:
                if s in positions:
                    first_modal(side)

        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'change_acon')))
        element.click()

    # Logout
    if (not stay_open) or (stay_open and side == 'Buy'):
        log_out(wait)
    return
