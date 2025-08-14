# /src/payoff_calculator.py

import numpy as np


def _calculate_leg_pl(price, leg):
    """Calculates the profit/loss for a single option leg."""
    pl = 0
    if leg['type'] == 'call':
        pl = np.maximum(0, price - leg['strike'])
    elif leg['type'] == 'put':
        pl = np.maximum(0, leg['strike'] - price)

    # P/L is payoff - premium for long positions, and premium - payoff for short positions
    if leg['action'] == 'buy':
        pl -= leg['premium']
    else:  # sell
        pl = leg['premium'] - pl

    return pl * leg['contracts'] * 100  # Standard contract size


def calculate_strategy_pl(strategy_legs, underlying_price_range):
    """
    Calculates the total profit/loss for a multi-leg strategy across a range of prices.
    """
    total_pl = np.zeros_like(underlying_price_range, dtype=float)

    for leg in strategy_legs:
        total_pl += _calculate_leg_pl(underlying_price_range, leg)

    # Calculate key metrics
    max_profit = np.max(total_pl)
    max_loss = np.min(total_pl)

    # Find break-even points (where P/L crosses zero)
    # This is a numerical approximation
    sign_change = np.where(np.diff(np.sign(total_pl)))[0]
    break_evens = []
    for idx in sign_change:
        # Linear interpolation to find a more accurate break-even point
        p1, p2 = underlying_price_range[idx], underlying_price_range[idx+1]
        pl1, pl2 = total_pl[idx], total_pl[idx+1]
        if pl1 * pl2 < 0:  # Ensure it's a zero crossing
            be = p1 - pl1 * (p2 - p1) / (pl2 - pl1)
            break_evens.append(be)

    return {
        "prices": underlying_price_range,
        "pnl": total_pl,
        "max_profit": max_profit if max_profit != np.inf else "Unlimited",
        "max_loss": max_loss if max_loss != -np.inf else "Unlimited",
        "break_evens": break_evens
    }
