import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Real-Time Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# Auto-refresh every 60 seconds
st_autorefresh(interval=60_000)

# --------------------------------------------------
# Helper: Market status
# --------------------------------------------------
def market_status():
    eastern = pytz.timezone("US/Eastern")
    now = datetime.now(eastern)

    if now.weekday() >= 5:
        return "Market Closed (Weekend)"
    if now.hour < 9 or (now.hour == 9 and now.minute < 30):
        return "Pre-Market"
    if 9 <= now.hour < 16:
        return "Market Open"
    return "After Hours"

# --------------------------------------------------
# Cached live data fetch (cloud-safe)
# --------------------------------------------------
@st.cache_data(ttl=60)
def fetch_live_data(symbol):
    df = yf.download(
        tickers=symbol,
        period="1d",
        interval="1m",
        prepost=True,
        progress=False
    )
    return df

# --------------------------------------------------
# UI: Title and context
# --------------------------------------------------
st.title("📊 Real-Time Stock Market Dashboard")

status = market_status()
st.info(f"🕒 {status}")

st.caption(
    "Live stock prices with pre-market and after-hours data. "
    "After-hours updates may be less frequent due to lower trading volume."
)

# --------------------------------------------------
# Sidebar controls
# --------------------------------------------------
st.sidebar.header("Controls")

symbols = ["AAPL", "MSFT", "GOOGL"]
selected_symbol = st.sidebar.selectbox("Select Stock", symbols)

ma_window = st.sidebar.slider(
    "Moving Average Window",
    min_value=3,
    max_value=20,
    value=5
)

# --------------------------------------------------
# Fetch data
# --------------------------------------------------
df = fetch_live_data(selected_symbol)

if df.empty:
    st.warning("No data available right now. Please try again later.")
    st.stop()

# --------------------------------------------------
# Fix: Flatten MultiIndex columns (yfinance cloud issue)
# --------------------------------------------------
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

df = df.copy()

# --------------------------------------------------
# Analysis
# --------------------------------------------------
df["MA"] = df["Close"].rolling(ma_window).mean()

latest_price = float(df["Close"].iloc[-1])
start_price = float(df["Close"].iloc[0])
price_change = latest_price - start_price

day_high = df["High"].max()
day_low = df["Low"].min()

# --------------------------------------------------
# Metrics
# --------------------------------------------------
col1, col2 = st.columns(2)

col1.metric(
    "Latest Price",
    f"${latest_price:.2f}"
)

col2.metric(
    "Change Today",
    f"${price_change:.2f}"
)

# --------------------------------------------------
# Interactive Chart: Price + MA + Volume + High/Low
# --------------------------------------------------
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3]
)

# Price line
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        name="Price",
        line=dict(width=2),
        hovertemplate="Time: %{x}<br>Price: $%{y:.2f}<extra></extra>"
    ),
    row=1,
    col=1
)

# Moving Average
fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA"],
        mode="lines",
        name=f"MA ({ma_window})",
        line=dict(width=2, dash="dot"),
        hovertemplate="Time: %{x}<br>MA: $%{y:.2f}<extra></extra>"
    ),
    row=1,
    col=1
)

# Volume bars
fig.add_trace(
    go.Bar(
        x=df.index,
        y=df["Volume"],
        name="Volume",
        marker=dict(opacity=0.4),
        hovertemplate="Time: %{x}<br>Volume: %{y:,}<extra></extra>"
    ),
    row=2,
    col=1
)

# Day High / Low bands
fig.add_hline(
    y=day_high,
    line=dict(width=1, dash="dash"),
    annotation_text="Day High",
    annotation_position="top left"
)

fig.add_hline(
    y=day_low,
    line=dict(width=1, dash="dash"),
    annotation_text="Day Low",
    annotation_position="bottom left"
)

# Layout polish
fig.update_layout(
    height=550,
    template="plotly_dark",
    hovermode="x unified",
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
)

fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
fig.update_yaxes(title_text="Volume", row=2, col=1)

st.subheader(f"{selected_symbol} Price Trend")
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Data source: Yahoo Finance · Built with Streamlit · "
    "Designed for real-time market monitoring and analysis."
)