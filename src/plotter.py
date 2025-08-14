# /src/plotter.py

import plotly.graph_objects as go


def plot_payoff_diagram(pnl_data):
    """
    Creates an interactive 2D payoff diagram using Plotly.
    """
    fig = go.Figure()

    # Add P&L line
    fig.add_trace(go.Scatter(
        x=pnl_data['prices'],
        y=pnl_data['pnl'],
        mode='lines',
        name='Profit/Loss',
        line=dict(color='royalblue', width=3)
    ))

    # Add zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    # Add break-even points
    for be in pnl_data['break_evens']:
        fig.add_vline(x=be, line_dash="dot", line_color="red", annotation_text=f"BE: {
                      be:.2f}", annotation_position="top left")

    fig.update_layout(
        title="Options Strategy Payoff Diagram",
        xaxis_title="Underlying Price at Expiration ($)",
        yaxis_title="Profit / Loss ($)",
        hovermode="x unified"
    )
    return fig


def plot_volatility_surface(df):
    """
    Creates an interactive 3D volatility surface plot using Plotly.
    """
    if df.empty or 'implied_volatility' not in df.columns or df['implied_volatility'].isnull().all():
        return go.Figure().update_layout(title="Not enough data to plot volatility surface.")

    # Pivot data for surface plot
    # We may need to handle cases where the grid is not perfectly rectangular
    # A meshgrid approach is more robust for scattered data, but pivot is simpler if it works
    try:
        pivot_df = df.pivot(
            index='strike', columns='time_to_expiration', values='implied_volatility')

        fig = go.Figure(data=[go.Surface(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='Viridis',
            colorbar=dict(title='Implied Volatility')
        )])

        fig.update_layout(
            title='Implied Volatility Surface',
            scene=dict(
                xaxis_title='Time to Expiration (Years)',
                yaxis_title='Strike Price ($)',
                zaxis_title='Implied Volatility (%)'
            ),
            margin=dict(l=40, r=40, b=40, t=80)
        )
    except Exception as e:
        # Fallback to a 3D scatter plot if pivoting fails (e.g., duplicate index/column pairs)
        fig = go.Figure(data=[go.Scatter3d(
            x=df['time_to_expiration'],
            y=df['strike'],
            z=df['implied_volatility'],
            mode='markers',
            marker=dict(
                size=4,
                color=df['implied_volatility'],
                colorscale='Viridis',
                colorbar_title='Implied Volatility',
                showscale=True
            )
        )])
        fig.update_layout(
            title='Implied Volatility Points (Scatter)',
            scene=dict(
                xaxis_title='Time to Expiration (Years)',
                yaxis_title='Strike Price ($)',
                zaxis_title='Implied Volatility (%)'
            ),
            margin=dict(l=40, r=40, b=40, t=80)
        )

    return fig
