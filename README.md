# Options Strategy & Volatility Surface Visualizer

A sophisticated quantitative finance tool built with Python to model and visualize two critical aspects of options trading: strategy payoffs and market-implied volatility.

Payoff Diagram Screenshot
<img width="1395" height="834" alt="Screenshot 2025-08-14 at 8 10 53 PM" src="https://github.com/user-attachments/assets/a280db65-a875-4ca0-b9f9-6fa9633bf249" />
<img width="1392" height="836" alt="Screenshot 2025-08-14 at 8 10 35 PM" src="https://github.com/user-attachments/assets/95a29d2a-59fa-4c8e-b8c6-e8707f3340dc" />




Volatility Surface Screenshot
<img width="1394" height="836" alt="Screenshot 2025-08-14 at 8 11 13 PM" src="https://github.com/user-attachments/assets/19455a81-0d21-4e00-8a44-c02413fcb976" />


---

##  Key Features

1.  **Options Strategy Payoff Visualizer:**
    *   Dynamically build multi-leg options strategies (e.g., Straddles, Iron Condors, Spreads).
    *   Generates an interactive 2D Profit/Loss diagram.
    *   Automatically calculates and displays key metrics: **Maximum Profit**, **Maximum Loss**, and **Break-Even Point(s)**.

2.  **Implied Volatility (IV) Surface Visualizer:**
    *   Fetches the complete options chain for any user-specified stock ticker from live market data.
    *   Calculates the implied volatility for every contract using the Black-Scholes-Merton model and a numerical root-finding algorithm.
    *   Renders an interactive 3D surface plot, visualizing the **volatility smile/skew** across all strikes and expirations.

---

##  Core Concepts & Skills Demonstrated

This project showcases a deep understanding of concepts central to quantitative finance and data science:

*   **Quantitative Finance:** Derivatives pricing (Black-Scholes-Merton), multi-leg P/L calculation, options greeks (implied volatility/vega).
*   **Numerical Methods:** Implementation of a numerical solver (`scipy.optimize.brentq`) to find the root of a complex, non-linear equation.
*   **Data Engineering:** Fetching, parsing, cleaning, and structuring complex, nested financial data (options chains) into a usable format.
*   **Advanced Data Visualization:** Conveying complex, multi-dimensional financial data in an intuitive and interactive format using Plotly.

---

##  Tech Stack

*   **Language:** Python
*   **Data Analysis & Computation:** Pandas, NumPy, SciPy
*   **Data Acquisition:** yfinance
*   **Visualization & UI:** Plotly, Streamlit

---

##  Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/deepsr2003/YOUR-REPO-NAME.git
    cd YOUR-REPO-NAME
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

---

##  How to Run

From the project's root directory, run the following command in your terminal:

```bash
streamlit run app.py
