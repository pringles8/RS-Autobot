def fid_buy(stocks):
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

    def fid_buy_modal():
        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
        element.click()

        # Loop through stocks
        for s in stocks:
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

    driver = uc.Chrome()
    driver.get("https://fidelity.com")
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "last-child")))
    element.click()

    # Login
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fs-mask-username")))
    element.send_keys(os.getenv("FIDELITY_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIDELITY_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'fs-login-button')))
    element.click()

    # Get all accounts
    accounts = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "acct-selector__acct-title"]')))

    # Loop through accounts
    for account in accounts:
        account.click()

        if not exclusions():
            fid_buy_modal()

    print("Bought ", RS.keys(), " in Fidelity")

    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "pntlt"]')))
    element = element.find_element(By.XPATH, '//a[@target = "_top"]')
    element.click()

    # Close
    driver.quit()

def fid_sell(stocks):
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

    def fid_sell_modal():
        # Open Trade Modal
        element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Trade")))
        element.click()

        # Loop through stocks
        for s in stocks:
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

    driver = uc.Chrome()
    driver.get("https://fidelity.com")
    wait = WebDriverWait(driver, 10)

    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "last-child")))
    element.click()

    # Login
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "fs-mask-username")))
    element.send_keys(os.getenv("FIDELITY_USERNAME"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'password')))
    element.send_keys(os.getenv("FIDELITY_PASSWORD"))
    element = wait.until(EC.element_to_be_clickable((By.ID, 'fs-login-button')))
    element.click()

    # Get all accounts
    accounts = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@class = "acct-selector__acct-title"]')))

    # Loop through accounts
    for account in accounts:
        account.click()

        if not exclusions():
            fid_sell_modal()

    print("Sold ", RS.keys(), " in Fidelity")

    # Logout
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class = "pntlt"]')))
    element = element.find_element(By.XPATH, '//a[@target = "_top"]')
    element.click()

    # Close
    driver.quit()