import yfinance as yf
import sqlite3
from datetime import datetime
import time

SYMBOLS = ["AAPL", "MSFT", "GOOGL"]

def create_table():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            time TEXT,
            symbol TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

def fetch_stock_price(symbol):
    data = yf.download(
        tickers=symbol,
        period="1d",
        interval="1m",
        prepost=True,     # 🔑 this enables after-hours
        progress=False
    )

    if data.empty:
        return None

    price = data["Close"].iloc[-1]
    return datetime.now(), symbol, float(price.item())

def save_price(time_val, symbol, price):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stock_prices VALUES (?, ?, ?)",
        (time_val, symbol, price)
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()

    while True:
        for symbol in SYMBOLS:
            result = fetch_stock_price(symbol)
            if result is None:
                continue

            time_now, sym, price = result
            save_price(time_now, sym, price)
            print(f"Saved: {sym} {price}")

        time.sleep(120)  # fetch every minute