# /src/config.py

# Default values for the Streamlit UI
DEFAULT_TICKER = 'SPY'
DEFAULT_RISK_FREE_RATE = 0.05  # 5%

# Plotting constants
# Show prices +/- 20% from current stock price
PAYOFF_CHART_X_RANGE_PERCENT = 0.20

# Solver constants for Implied Volatility calculation
VOL_SOLVER_BOUNDS = (1e-5, 4.0)  # IV bounds from 0.001% to 400%
