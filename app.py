# /app.py

import streamlit as st
import pandas as pd
import numpy as np

from src.config import DEFAULT_TICKER, DEFAULT_RISK_FREE_RATE, PAYOFF_CHART_X_RANGE_PERCENT
from src.data_fetcher import get_full_option_chain, get_stock_price
from src.payoff_calculator import calculate_strategy_pl
from src.quant_tools import calculate_iv_for_chain
from src.plotter import plot_payoff_diagram, plot_volatility_surface

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Options Strategy & Volatility Visualizer",
    page_icon="📈",
    layout="wide"
)

# --- Session State Initialization ---
if 'strategy_legs' not in st.session_state:
    st.session_state.strategy_legs = []

# --- Sidebar for Global Inputs ---
st.sidebar.title("Configuration")
ticker_symbol = st.sidebar.text_input(
    "Stock Ticker", value=DEFAULT_TICKER).upper()
risk_free_rate = st.sidebar.slider(
    "Risk-Free Rate (%)", 0.0, 10.0, DEFAULT_RISK_FREE_RATE * 100, 0.1) / 100

st.title("Options Strategy & Volatility Visualizer")
st.markdown(f"**Analyzing Ticker: `{ticker_symbol}`**")

# --- Main Application Tabs ---
tab1, tab2 = st.tabs(["Strategy Payoff Visualizer",
                     "Implied Volatility Surface"])

# ==================================================================================================
# TAB 1: STRATEGY PAYOFF VISUALIZER
# ==================================================================================================
with tab1:
    st.header("Build Your Options Strategy")

    # --- Strategy Input UI ---
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 0.5])
    with col1:
        if st.button("➕ Add Leg", use_container_width=True):
            st.session_state.strategy_legs.append({
                'action': 'buy', 'type': 'call', 'strike': 100.0, 'premium': 2.50, 'contracts': 1
            })

    if not st.session_state.strategy_legs:
        st.info("Click '➕ Add Leg' to start building your strategy.")
    else:
        # Display each leg with input fields
        for i, leg in enumerate(st.session_state.strategy_legs):
            st.markdown(f"--- \n **Leg {i+1}**")
            cols = st.columns([1, 1, 1.5, 1.5, 1, 0.5])
            leg['action'] = cols[0].selectbox("Action", ['buy', 'sell'], index=[
                                              'buy', 'sell'].index(leg['action']), key=f"action_{i}")
            leg['type'] = cols[1].selectbox("Type", ['call', 'put'], index=[
                                            'call', 'put'].index(leg['type']), key=f"type_{i}")
            leg['strike'] = cols[2].number_input(
                "Strike Price", min_value=0.0, value=leg['strike'], step=0.5, key=f"strike_{i}")
            leg['premium'] = cols[3].number_input(
                "Premium (Price)", min_value=0.0, value=leg['premium'], step=0.01, key=f"premium_{i}")
            leg['contracts'] = cols[4].number_input(
                "Contracts", min_value=1, value=leg['contracts'], step=1, key=f"contracts_{i}")
            if cols[5].button("🗑️", key=f"del_{i}"):
                st.session_state.strategy_legs.pop(i)
                st.experimental_rerun()

    st.markdown("---")

    # --- Calculation and Plotting ---
    if st.session_state.strategy_legs and st.button("📊 Generate Payoff Diagram", type="primary"):
        with st.spinner("Calculating payoff..."):
            current_price = get_stock_price(ticker_symbol)
            if current_price:
                price_range = np.linspace(
                    current_price * (1 - PAYOFF_CHART_X_RANGE_PERCENT),
                    current_price * (1 + PAYOFF_CHART_X_RANGE_PERCENT),
                    num=200
                )

                pnl_data = calculate_strategy_pl(
                    st.session_state.strategy_legs, price_range)

                # Display Metrics
                st.subheader("Strategy Metrics")
                metric_cols = st.columns(3)
                max_profit_str = f"${pnl_data['max_profit']:.2f}" if isinstance(
                    pnl_data['max_profit'], (int, float)) else pnl_data['max_profit']
                max_loss_str = f"${pnl_data['max_loss']:.2f}" if isinstance(
                    pnl_data['max_loss'], (int, float)) else pnl_data['max_loss']

                metric_cols[0].metric("Maximum Profit", max_profit_str)
                metric_cols[1].metric("Maximum Loss", max_loss_str)

                be_str = ", ".join(
                    [f"${be:.2f}" for be in pnl_data['break_evens']]) or "N/A"
                metric_cols[2].metric("Break-Even Points", be_str)

                # Display Plot
                fig = plot_payoff_diagram(pnl_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error(f"Could not fetch current price for {ticker_symbol}.")

# ==================================================================================================
# TAB 2: IMPLIED VOLATILITY SURFACE
# ==================================================================================================
with tab2:
    st.header("Implied Volatility Surface")
    st.info("This tool fetches the entire options chain and calculates the implied volatility for each contract to plot a 3D surface. This may take a few moments.")

    if st.button("🌋 Generate Volatility Surface", type="primary"):
        with st.spinner(f"Fetching options chain for {ticker_symbol} and calculating IV..."):
            data = get_full_option_chain(ticker_symbol)
            current_price = data['price']
            chain_df = data['chain']

            if current_price is None or chain_df.empty:
                st.error(f"Could not fetch options data for {
                         ticker_symbol}. It may not have options or the ticker is invalid.")
            else:
                # Calculate IV for the entire chain
                iv_df = calculate_iv_for_chain(
                    chain_df, current_price, risk_free_rate)

                # Filter out any rows where IV calculation failed
                iv_df.dropna(subset=['implied_volatility'], inplace=True)

                # Convert IV to percentage for plotting
                iv_df['implied_volatility'] *= 100

                st.success(f"Successfully calculated IV for {
                           len(iv_df)} contracts.")

                # Display Plot
                fig = plot_volatility_surface(iv_df)
                st.plotly_chart(fig, use_container_width=True)

                # Optional: Display raw data
                if st.checkbox("Show Raw Data with Implied Volatility"):
                    st.dataframe(iv_df[['strike', 'expirationDate', 'option_type',
                                 'lastPrice', 'time_to_expiration', 'implied_volatility']].head(20))
