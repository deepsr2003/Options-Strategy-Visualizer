# /src/quant_tools.py

import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from src.config import VOL_SOLVER_BOUNDS


def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    """
    Calculates the Black-Scholes-Merton price of a European option.

    S: Current stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free interest rate
    sigma: Volatility (annualized)
    option_type: 'call' or 'put'
    """
    if T <= 0:  # Handle expired options
        return max(0, S - K) if option_type == 'call' else max(0, K - S)
    if sigma <= 0:  # Handle zero volatility
        return max(0, S - K) if option_type == 'call' else max(0, K - S)

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    elif option_type == 'put':
        price = (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    else:
        raise ValueError("Invalid option type. Must be 'call' or 'put'.")
    return price


def _iv_objective_function(sigma, S, K, T, r, market_price, option_type):
    """Objective function for the solver: (BSM price - market price)."""
    return black_scholes_price(S, K, T, r, sigma, option_type) - market_price


def calculate_implied_volatility(S, K, T, r, market_price, option_type='call'):
    """
    Calculates the implied volatility using the Brentq root-finding algorithm.
    """
    try:
        iv = brentq(
            f=_iv_objective_function,
            a=VOL_SOLVER_BOUNDS[0],
            b=VOL_SOLVER_BOUNDS[1],
            args=(S, K, T, r, market_price, option_type)
        )
    except ValueError:
        # If solver fails (e.g., market price is outside theoretical bounds), return NaN
        iv = np.nan
    return iv


def calculate_iv_for_chain(df, current_price, risk_free_rate):
    """
    Applies the IV calculation to each row of an options chain DataFrame.
    """
    # Vectorized calculation for efficiency is possible but more complex to set up with a solver.
    # .apply is clear and sufficient for this use case.
    df['implied_volatility'] = df.apply(
        lambda row: calculate_implied_volatility(
            S=current_price,
            K=row['strike'],
            T=row['time_to_expiration'],
            r=risk_free_rate,
            market_price=row['lastPrice'],
            option_type=row['option_type']
        ),
        axis=1
    )
    return df
