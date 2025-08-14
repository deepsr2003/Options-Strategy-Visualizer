# /src/data_fetcher.py

import yfinance as yf
import pandas as pd
from datetime import datetime


def get_stock_price(ticker_symbol):
    """Fetches the current stock price."""
    ticker = yf.Ticker(ticker_symbol)
    todays_data = ticker.history(period='1d')
    return todays_data['Close'][0] if not todays_data.empty else None


def get_full_option_chain(ticker_symbol):
    """
    Fetches the entire option chain (all expirations) for a given ticker.
    Returns a dictionary with current price and the options DataFrame.
    """
    ticker = yf.Ticker(ticker_symbol)

    # Get current stock price
    current_price = get_stock_price(ticker_symbol)
    if current_price is None:
        return {'price': None, 'chain': pd.DataFrame()}

    # Get all available expiration dates
    expirations = ticker.options
    if not expirations:
        return {'price': current_price, 'chain': pd.DataFrame()}

    all_chains = []
    today = datetime.now()

    for exp in expirations:
        # Get option chain for a specific expiration
        opt = ticker.option_chain(exp)

        # Combine calls and puts
        calls = opt.calls
        calls['option_type'] = 'call'
        puts = opt.puts
        puts['option_type'] = 'put'

        chain = pd.concat([calls, puts])
        chain['expirationDate'] = pd.to_datetime(exp)

        all_chains.append(chain)

    if not all_chains:
        return {'price': current_price, 'chain': pd.DataFrame()}

    # Concatenate all dataframes and calculate time to expiration
    full_chain = pd.concat(all_chains)
    full_chain['time_to_expiration'] = (
        full_chain['expirationDate'] - today).dt.days / 365.25

    # Filter out contracts with no volume or open interest as they are not reliable
    full_chain = full_chain[
        (full_chain['volume'] > 0) & (full_chain['openInterest'] > 0)
    ].copy()

    return {'price': current_price, 'chain': full_chain}
