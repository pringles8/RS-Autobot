import os
'''
import tastytrade_api
from tastytrade_api.authentication import TastytradeAuth
from tastytrade_api.account.account_handler import TastytradeAccount

username = os.getenv("FIRSTRADE_USERNAME")
password = os.getenv("FIRSTRADE_PASSWORD")

# Initialize the authentication object
auth = TastytradeAuth(username, password)

# Log in to the API
auth_data = auth.login()

if auth_data:
    print("Successfully logged in!")
else:
    print("Failed to log in.")

# Validate the session
is_valid = auth.validate_session()

if is_valid:
    print("Session is valid.")
else:
    print("Session is invalid or expired.")

# Print accounts
account = TastytradeAccount(auth.session_token, "https://api.tastytrade.com")
accounts = account.get_accounts()
print(accounts)

# Destroy the session (log out)
if auth.destroy_session():
    print("Successfully logged out.")
else:
    print("Failed to log out.")
'''

from tastyworks.models import option_chain, underlying
from tastyworks.models.greeks import Greeks
from tastyworks.models.option import Option, OptionType
from tastyworks.models.order import (Order, OrderDetails, OrderPriceEffect,
                                     OrderType)
from tastyworks.models.session import TastyAPISession
from tastyworks.models.trading_account import TradingAccount
from tastyworks.models.underlying import UnderlyingType
from tastyworks.streamer import DataStreamer
from tastyworks.tastyworks_api import tasty_session
from tastyworks.utils import get_third_friday