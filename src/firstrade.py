import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

load_dotenv()


def open_website(driver, wait):
    driver.get("https://www.firstrade.com/content/en-us/welcome")
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log In")))
    element.click()
    return


def log_in(wait, num_acct):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    element.send_keys(os.getenv("FIRSTRADE_USERNAME").split(",")[num_acct].strip())
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIRSTRADE_PASSWORD").split(",")[num_acct].strip())
    element = wait.until(EC.element_to_be_clickable((By.ID, 'loginButton')))
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
    print('First Logout Complete.')
    return


def get_positions(wait):
    # Click positions
    positions = []

    #time.sleep(1)
    element = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, 'Positions')))
    wait.until(EC.staleness_of(element))
    element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Positions')))
    element.send_keys(Keys.ENTER)
    time.sleep(1)

    element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="content dashboard-block-content"]')))
    element = element[1]


    if element.text != "You do not have any positions.":
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//table[@id="home_positions_table"]'))) # time out - positions button not hit
        element = element.find_elements(By.XPATH, './/td[@class="ta_left"]')

        if isinstance(element, list):
            positions = [el.text for el in element]
        else:
            positions = [element.text]

    return positions


def first_buy_and_sell(driver, wait, buy=[], sell=[], acct=0):
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
        time.sleep(0.75)

        # Enter quantity
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quantity"]')))
        element.send_keys(1)

        # Enter ticker and limit prices
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="quoteSymbol"]')))
        element.clear()
        element.send_keys(stock)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="getQ"]')))
        element.click()
        time.sleep(0.75)

        # Send order
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@id="submitOrder"]')))
        element.click()

        # Place another order
        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@class="submitted_placeorder_bnt btn btn-action"]')))
        element.click()

        # Perhaps clear ticket hear?
        time.sleep(1)
        return

    open_website(driver, wait)
    log_in(wait, acct)

    # Check for PIN //div[@class="subtitle"]
    if driver.current_url == "https://invest.firstrade.com/cgi-bin/enter_pin?destination_page=home":
        for i in os.getenv('FIRSTRADE_PIN').split(",")[acct].strip():
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title={}]".format(i))))
            element.click()

        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="submit"]')))
        element.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="logout btn btn-clear-blue"]')))

    # Make sure we are on the home page
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/cgi-bin/home"]')))
    element.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@class="title_list dashboard-column-title"]')))

    # Scroll Down
    driver.execute_script("window.scrollTo(0,200)")

    # Open Trade Modal
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="javascript:ChangeOrderbar();"]')))
    element.click()

    # Get all accounts
    select = Select(wait.until(EC.visibility_of_element_located((By.XPATH, '//select[@id="accountId"]'))))
    options = select.options

    # Loop through accounts and buy
    for i in range(len(options)):
        select.select_by_index(i)

        positions = get_positions(wait)

        if len(buy) > 0:
            for stock in buy:
                if stock not in positions:
                    first_modal(side="Buy")
                    print('Bought ', stock, " in First account " + str(options[i].text)[-4:])
            print("First buying complete in account " + str(options[i].text)[-4:])
        if len(sell) > 0:
            for stock in sell:
                if stock in positions:
                    first_modal(side="Sell")
                    print('Sold ', stock, " in First account " + str(options[i].text)[-4:])
            print("First selling complete in account " + str(options[i].text)[-4:])

    # Logout
    time.sleep(1)
    log_out(wait)

    num_accts = len(os.getenv("FIRSTRADE_USERNAME").split(","))
    if num_accts != acct + 1:
        acct += 1
        first_buy_and_sell(buy=buy, sell=sell, driver=driver, wait=wait, acct=acct)

    return
