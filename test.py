import robin_stocks.robinhood as robin
import sys
import pyotp
from config import ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD, ROBINHOOD_MFA_SECRET

# Attempt to login without MFA
print("Attempting to login without MFA...")
try:
    login = robin.login(ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD, store_session=False)
    print("Login successful without MFA.")
except Exception as e:
    print(f"Login without MFA failed: {e}")
    # Generate TOTP
    totp = pyotp.TOTP(ROBINHOOD_MFA_SECRET).now()
    print(f"Generated TOTP: {totp}")
    # Attempt to login with MFA
    try:
        login = robin.login(ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD, mfa_code=totp, store_session=False)
        print("Login successful with MFA.")
    except KeyError as e:
        print(f"KeyError during login with MFA: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during login with MFA: {e}")
        sys.exit(1)

# View profile
def view_profile():
    profile_basics = robin.account.build_user_profile()
    print(profile_basics)

# Fetch and print portfolio
my_portfolio = robin.build_holdings()
print("Fetched portfolio data.")

if not my_portfolio:
    print("No holdings found in the portfolio.")
else:
    for stock, details in my_portfolio.items():
        print(f"Stock: {stock}")
        print(f"Details: {details}")

# Uncomment to view profile
# view_profile()
