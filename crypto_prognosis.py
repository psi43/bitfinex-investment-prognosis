import requests  # Used for sending requests to an API
import hmac  # Provides functions for creating cryptographic hash-based message authentication codes
import hashlib  # Used for secure hashing algorithms (like SHA-256, SHA-384, etc.)
import time  # Provides functions to work with time (e.g., timestamps, delays)
import json  # Used for encoding and decoding the JSON data format
from datetime import datetime  # Used for adding timestamps to the debug log
from prettytable import PrettyTable  # Used to create tables for displaying information neatly
import argparse  # Used for parsing command-line arguments

API_KEY = "your_API_key"
API_SECRET = "your_API_secret"

BASE_URL = "https://api.bitfinex.com"


def get_headers(api_key, api_secret, path, payload=""):
    """
    Generates headers for the API request. These headers are required for authenticating
    the request with the Bitfinex API.

    :param api_key: API key from Bitfinex
    :param api_secret: API secret from Bitfinex
    :param path: API endpoint path
    :param payload: Request payload (optional)
    :return: Dictionary of headers
    """
    nonce = str(int(time.time() * 1000))
    signature = f"/api{path}{nonce}{payload}"
    h = hmac.new(api_secret.encode(), signature.encode(), hashlib.sha384)

    return {
        "bfx-apikey": api_key,
        "bfx-nonce": nonce,
        "bfx-signature": h.hexdigest(),
        "Content-Type": "application/json",
    }


def calculate_investment(wallets):
    """
    Calculates the total investment in USD from wallet trade details.

    :param wallets: List of wallet data from the API
    :return: Total investment in USD
    """
    total_investment = 0
    for wallet in wallets:
        for trade_index in [6, 7]:
            if len(wallet) > trade_index and wallet[trade_index]:
                trade_details = wallet[trade_index]
                if "trade_price" in trade_details and "trade_amount" in trade_details:
                    trade_price = float(trade_details["trade_price"])
                    trade_amount = abs(float(trade_details["trade_amount"]))
                    total_investment += trade_price * trade_amount
    return total_investment


def get_wallet_data(api_key, api_secret, debug_level=0):
    """
    Retrieves wallet balances and calculates total investment.

    :param api_key: API key from Bitfinex
    :param api_secret: API secret from Bitfinex
    :param debug_level: Debug level (0 = no debug, 1 = console, 2 = console + log, 3 = log only)
    :return: BTC balance, BTC value in USD, total investment
    """
    path = "/v2/auth/r/wallets"
    url = BASE_URL + path
    headers = get_headers(api_key, api_secret, path)

    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error retrieving wallet data: {response.text}")

    wallets = response.json()

    if debug_level in [1, 2]:
        print("Wallet Data:", json.dumps(wallets, indent=2))

    if debug_level in [2, 3]:
        with open("debug_log.txt", "w") as debug_file:
            debug_file.write(f"Debug Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            debug_file.write(json.dumps(wallets, indent=2))
        if debug_level == 2:
            print("Debug output has been saved to debug_log.txt")

    total_investment = calculate_investment(wallets)
    btc_balance = next(
        (float(wallet[2]) for wallet in wallets if wallet[0] == "exchange" and wallet[1].upper() == "BTC"), 0.0)
    return btc_balance, 0.0, total_investment


def get_current_btc_price():
    """
    Fetches the current BTC/USD price from the Bitfinex API.

    :return: Current BTC/USD price
    """
    url = "https://api.bitfinex.com/v2/ticker/tBTCUSD"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error retrieving BTC price: {response.text}")
    return response.json()[6]


def main():
    """
    Main function to calculate required BTC price for a target value.
    """
    parser = argparse.ArgumentParser(description="Analyze BTC investment data and calculate required price.")
    parser.add_argument("--target", type=float, help="Target value in USD (e.g., 200)", required=False)
    parser.add_argument("--debug-level", type=int, choices=[0, 1, 2, 3], default=0,
                        help="Set debug output level: 0 (none), 1 (console only), 2 (console + log), 3 (log only).")
    args = parser.parse_args()

    target_value = args.target if args.target else float(input("Enter your target value in USD (e.g., 200): "))
    debug_level = args.debug_level

    try:
        btc_balance, btc_usd_value, total_investment = get_wallet_data(API_KEY, API_SECRET, debug_level=debug_level)
        current_btc_price = get_current_btc_price()
        btc_usd_value = btc_balance * current_btc_price

        if debug_level == 1:
            print(f"Current BTC/USD price: {current_btc_price:.2f} $")

        required_btc_price = target_value / btc_balance if btc_balance > 0 else 0
        price_difference = required_btc_price - current_btc_price
        percentage_change = (price_difference / current_btc_price) * 100 if current_btc_price > 0 else 0

        overview_table = PrettyTable()
        overview_table.field_names = ["Description", "Value"]
        overview_table.add_row(["BTC Balance", f"{btc_balance:.8f} BTC"])
        overview_table.add_row(["Current Value (USD)", f"{btc_usd_value:.2f} $"])
        overview_table.add_row(["Total Investment (USD)", f"{total_investment:.2f} $"])
        print(overview_table)

        analysis_table = PrettyTable()
        analysis_table.field_names = ["Description", "Value"]
        analysis_table.add_row(["Target Value (USD)", f"{target_value:.2f} $"])
        analysis_table.add_row(["Current BTC Price", f"{current_btc_price:,.2f} $"])
        analysis_table.add_row(["Required BTC Price", f"{required_btc_price:,.2f} $"])
        analysis_table.add_row(["Price Difference", f"{price_difference:,.2f} $"])
        analysis_table.add_row(["Percentage Change", f"{percentage_change:.2f} %"])
        print(analysis_table)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()