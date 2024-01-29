import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

load_dotenv()

def open_website(driver):
    driver.get("https://secure.chase.com/web/auth/dashboard#/dashboard/overviewAccounts/overview/index")
    time.sleep(3)
    return

def log_in(wait):
    # Login
    element = wait.until(EC.element_to_be_clickable((By.ID, 'userId-text-input-field')))
    element.send_keys(os.getenv("CHASE_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password-text-input-field')))
    element.send_keys(os.getenv("CHASE_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'signin-button')))
    element.click()
    return
def chase_buy_and_sell(driver, wait, buy=[], sell=[], acct=0):
    '''
    Chase - using selenium to "manually" submit tickets.
    Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
    and submit -> after looped through accounts and stocks, logout

    TO-DO:
    '''

    def exclusions():
        return

    def chase_ticket(side):

        return

    open_website(driver)
    driver.switch_to.frame(driver.find_element(By.ID, 'logonbox'))
    log_in(wait)
    driver.switch_to.default_content()

    # Go to Trade Screen
    #driver.navigate().to("https://secure.chase.com/web/auth/dashboard#/dashboard/oi-trade/equity/entry")
    #time.sleep(5)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="navigation-bar-item"]')))
    element.click()
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="navigation-bar-menu-item navigation-bar-menu-item--interactive"]')))
    element.click()

    # Get accounts - class="list-item__container"
    element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="list-item__container"]')))
    print(element)

    # Loop through buy and sell for each account
    if len(buy) > 0:
        for s in buy:
            chase_ticket("Buy")
    if len(sell) > 0:
        for s in sell:
            chase_ticket("Sell")

