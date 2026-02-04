import streamlit as st
import pandas as pd
import sqlite3
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Real-Time Stock Dashboard",
    page_icon="📊",
    layout="wide"
)
st_autorefresh(interval=5000)

st.title("📈 Real-Time Stock Market Dashboard")

st.caption(
    "Live market data ingested in real time. Includes regular, after-hours, and pre-market data. "
    "Dashboard updates automatically and highlights short-term trends."
    "After-hours prices update less frequently due to lower trading volume."
)

st.sidebar.header("Controls")

conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM stock_prices", conn)
df["time"] = pd.to_datetime(df["time"])

stocks = df["symbol"].unique().tolist()
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

ma_window = st.sidebar.slider(
    "Moving Average Window",
    min_value=3,
    max_value=20,
    value=5
)

filtered_df = df[df["symbol"] == selected_stock]

latest_price = filtered_df["price"].iloc[-1]
price_change = latest_price - filtered_df["price"].iloc[0]

col1, col2 = st.columns(2)
col1.metric("Latest Price", round(latest_price, 2))
col2.metric("Change Since Start", round(price_change, 2))

filtered_df["MA"] = filtered_df["price"].rolling(ma_window).mean()

st.subheader(f"{selected_stock} Price Trend")

st.line_chart(
    filtered_df.set_index("time")[["price", "MA"]],
    height=400
)
