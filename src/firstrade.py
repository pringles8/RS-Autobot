import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

load_dotenv()

def open_website(driver, wait):
    driver.get("https://www.firstrade.com/content/en-us/welcome")
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log In")))
    element.click()
    return

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    element.send_keys(os.getenv("FIRSTRADE_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIRSTRADE_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'loginButton')))
    element.click()
    return

def log_out(wait):
    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="logout btn btn-clear-blue"]')))
    element.click()
    print('First Logout Complete.')
    return

def get_positions(wait, driver):
    # Click positions
    positions = []
    '''
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn-white"]')))
    try:
        wait.until(EC.staleness_of(element))
    except:
        print("Exception")
        
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn-white"]')))
    '''
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Positions')))
    print(element)
    wait.until(EC.staleness_of(element))
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Positions')))
    #ActionChains(driver).move_to_element(element).click(element).perform()  # Stale, maybe try the div
    element.click()
    # Try drive.get
    '''
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn-white"]')))
    if EC.staleness_of(element):
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn-white"]')))

    #element.click()
    print(element)
    ActionChains(driver).move_to_element(element).click(element).perform() #Stale, maybe try the div
    '''

    element = wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@id="home_positions_table"]')))
    element = element.find_elements((By.XPATH, '//td[@class="ta_left"]'))

    if isinstance(element, list):
        positions = [el.text for el in element]
    else:
        positions = [element.text]

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
        # Press buy/sell radio button
        buy_sell_xpath = "transactionType_Buy" if side == "Buy" else "transactionType_Sell"
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="{}"]'.format(buy_sell_xpath))))
        element.click()

        # Enter quantity
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quantity"]')))
        element.send_keys(1)

        # Enter ticker and limit prices
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quoteSymbol"]')))
        element.clear()
        element.send_keys(s)
        time.sleep(3)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="getQ"]')))
        element.click()

        # Send order
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="submitOrder"]')))
        #element.click()

        # Place another order
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="submitted_placeorder_bnt btn btn-action"]')))
        element.click()

        # Perhaps clear ticket hear?
        return

    if (not stay_open) or (stay_open and side == 'Buy'):
        open_website(driver, wait)
        log_in(wait)

    # Check for PIN //div[@class="subtitle"]
    if driver.current_url == "https://invest.firstrade.com/cgi-bin/enter_pin?destination_page=home":
        for i in os.getenv('FIRSTRADE_PIN'):
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title={}]".format(i))))
            element.click()

        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="submit"]')))
        element.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="logout btn btn-clear-blue"]')))

    # Make sure we are on the home page
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/cgi-bin/home"]')))
    element.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="title_list dashboard-column-title"]')))

    # Open Trade Modal
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="javascript:ChangeOrderbar();"]')))
    element.click()

    # Get all accounts
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@id="accountId"]'))))
    options = select.options

    # Loop through accounts and buy
    for i in range(len(options)):
        select.select_by_index(i)

        positions = get_positions(wait, driver)

    # Logout -------------------------------------------
    if (not stay_open) or (stay_open and side == 'Buy'):
        log_out(wait)
    return
