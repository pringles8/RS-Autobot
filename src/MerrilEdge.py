import os
from dotenv import load_dotenv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

load_dotenv()

def open_website(driver):
    driver.get("https://www.merrilledge.com/")
    time.sleep(3)
    return

def log_in(wait, num_acct):
    element = wait.until(EC.element_to_be_clickable((By.ID, 'ULinksLogin')))
    element.click()
    time.sleep(3)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="oid"]')))
    element.send_keys(os.getenv("MERRIL_USERNAME").split(",")[num_acct].strip())
    time.sleep(3)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@id="pass"]')))
    element.send_keys(os.getenv("MERRIL_PASSWORD").split(",")[num_acct].strip())
    time.sleep(3)
    return

def get_positions(wait):
    try:
        element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//a[@title= "Click here to prefill"]')))
    except:
        element = []

    if isinstance(element, list):
        positions = [el.text for el in element]
    else:
        positions = [element.text]

    return positions

def merril_buy_and_sell(driver, wait, buy=[], sell=[], acct=0):
    '''
        Merril - using selenium to "manually" submit tickets.
        Process: login -> loop through accounts -> check if they can trade stocks -> open trade ticket
        and submit -> after looped through accounts and stocks, logout

        TO-DO:
        - Loop through accounts for each stock instead of looping through stocks per account since the ticket is saved
        across accounts
        '''
    def merril_ticket(side):
        # Choose buy or sell
        select = Select(wait.until(EC.visibility_of_element_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_ddlOrderType'))))
        select.select_by_index(1) if side == "Buy" else select.select_by_index(2)

        # Enter Symbol  id="ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_txtSymbol"
        element = wait.until(EC.visibility_of_all_elements_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_txtSymbol')))
        element.send_keys(s)

        # Order Type ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_ddPriceType
        select = Select(wait.until(EC.visibility_of_element_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_ddPriceType'))))
        select.select_by_index(3) if side == "Buy" else select.select_by_index(1)

        if side == "Sell":
            # Sell all ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_cbSellAll
            element = wait.until(EC.visibility_of_all_elements_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_cbSellAll')))
            element.click()
        else:
            # Enter quantity ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_txtQuantity
            element = wait.until(EC.visibility_of_all_elements_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_txtQuantity')))
            element.send_keys(1)

            # Get limit price //span[@class="floatRight"]
            element = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//span[@class="floatRight"]')))
            element = element[7]
            lim_price = element.text
            lim_price = lim_price[1:5]

            # Input limit price ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_txtPrice
            element = wait.until(EC.visibility_of_all_elements_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_txtPrice')))
            element.send_keys(lim_price)

        # Duration ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_ddlExpiration
        select = Select(wait.until(EC.visibility_of_element_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_ddlExpiration'))))
        select.select_by_index(1)

        return

    open_website(driver)
    log_in(wait, acct)

    # Click "Trade" Tab - //a[@clickurlattribute="/Equities/OrderEntry.aspx"]
    #element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Trade')))
    #element.click()

    # Click "Stocks & ETFs" - href="/Equities/OrderEntry.aspx" or link_text = Stocks & ETFs
    driver.navigate.to("https://olui2.fs.ml.com/Equities/OrderEntry.aspx")

    # Get accounts //a[@aria-haspopup="listbox"]
    #select = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@aria-haspopup="listbox"]')))
    #element.click()

    # Accounts //a[contains(@href, "OrderEntry.aspx?as_cd=")]
    element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "OrderEntry.aspx?as_cd=")]')))
    endings = [el.getAttribute("asd") for el in element]

    for end in endings:
        driver.navigate.to("https://olui2.fs.ml.com/Equities/OrderEntry.aspx?as_cd=" + end)

        positions = get_positions(wait)

        if len(buy) > 0:
            for s in buy:
                if s not in positions:
                    merril_ticket("Buy")
        if len(sell) > 0:
            for s in sell:
                if s in positions:
                    merril_ticket("Sell")

        # Press Preview ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_resxlblOrderPreviewText
        element = wait.until(EC.visibility_of_element_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_resxlblOrderPreviewText')))
        element.click()

        # Press Submit ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_EquitiesResourceLabel2
        element = wait.until(EC.visibility_of_element_located((By.ID, 'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_EquitiesResourceLabel2')))
        #element.click()

        # Press new order ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_resxlblPlaceNewOrder
        element = wait.until(EC.visibility_of_element_located((By.ID,'ctl00_ctl00_ctl01_cphSiteMst_cphNestedPage_cphStage_view1_PilotPreviewConfirmPage_resxlblPlaceNewOrder')))
        #element.click()

    # Log out
    element = wait.until(EC.visibility_of_element_located((By.ID,'globalnavlogout')))
    element.click()

    num_accts = len(os.getenv("MERRIL_USERNAME").split(","))
    if num_accts != acct + 1:
        acct += 1
        merril_buy_and_sell(buy=buy, sell=sell, driver=driver, wait=wait, acct=acct)

    return
