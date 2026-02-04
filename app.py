import streamlit as st
import pandas as pd
import yfinance as yf
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import pytz

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

# 🔧 FIX: flatten yfinance MultiIndex columns (cloud-safe)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# --------------------------------------------------
# Analysis
# --------------------------------------------------
df = df.copy()
df["MA"] = df["Close"].rolling(ma_window).mean()

# --------------------------------------------------
# Metrics
# --------------------------------------------------
latest_price = float(df["Close"].iloc[-1])
start_price = float(df["Close"].iloc[0])
price_change = latest_price - start_price

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
# Chart
# --------------------------------------------------
st.subheader(f"{selected_symbol} Price Trend")

st.line_chart(
    df[["Close", "MA"]],
    height=400
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.caption(
    "Data source: Yahoo Finance · Built with Streamlit · "
    "Designed for real-time market monitoring and analysis."
)