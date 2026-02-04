📊 Real-Time Stock Market Dashboard

A real-time, interactive stock market dashboard built with Streamlit, Yahoo Finance, and Plotly.
It visualizes live, pre-market, and after-hours stock data with professional-grade charts and analytics.

🔗 Live Demo: https://real-time-stock-dashboard-47tavmrgk52nukib9fj8vc.streamlit.app/

🚀 Features

Live price updates (auto-refresh every 60 seconds)

Pre-market & after-hours data support

Interactive price chart with zoom, pan, and hover tooltips

Moving average overlay (configurable window)

Volume bars, color-coded by price movement

Intraday high & low bands for quick market context

Dark-mode UI optimized for financial data

Cloud-safe architecture (no background jobs or local databases)

🧠 Why This Project Matters

This project was designed to go beyond a basic demo:

Uses on-demand data fetching with caching instead of background workers

Handles real-world API quirks (Yahoo Finance MultiIndex columns)

Built specifically to run reliably on Streamlit Cloud

Focuses on data clarity and visual hierarchy, not just raw plots

It reflects how production dashboards are actually built and deployed.

🛠 Tech Stack

Python

Streamlit – UI & app framework

Yahoo Finance (yfinance) – live market data

Plotly – interactive, professional-grade charts

Pandas – data manipulation

Streamlit Cloud – deployment

📈 Dashboard Overview

Top section

Current market status (Pre-market / Open / After-hours)

Latest price

Net price change for the day

Main chart

Smooth price curve

Moving average overlay

Day high / day low reference lines

Interactive tooltips

Bottom section

Volume bars

Green = upward price movement

Red = downward price movement

⚙️ How It Works

User selects a stock symbol and moving average window

App fetches live intraday data from Yahoo Finance

Data is cached for 60 seconds to reduce API load

Columns are normalized to handle Yahoo Finance edge cases

Metrics and charts are rendered using Plotly

App auto-refreshes to keep data current

No local storage. No cron jobs. No fragile dependencies.

🧩 Architecture Decisions

Why no database?
Streamlit Cloud runs apps in ephemeral containers. Local databases and background ingestion jobs are unreliable in this environment.
Instead, this app fetches live data on demand and caches results briefly.

Why Plotly instead of st.line_chart?
Plotly provides:

Better interactivity

Hover tooltips

Zooming and panning

Cleaner financial-style visuals

▶️ Run Locally
git clone https://github.com/<your-username>/real-time-stock-dashboard.git
cd real-time-stock-dashboard


pip install -r requirements.txt
streamlit run app.py
📦 Requirements
streamlit
pandas
yfinance
pytz
streamlit-autorefresh
plotly
🌐 Deployment

The app is deployed using Streamlit Cloud.

Steps:

Push the repo to GitHub

Create a new app on Streamlit Cloud

Select app.py as the entry point

Deploy — the app auto-redeploys on every push

🧪 Known Limitations

After-hours data may update less frequently due to low trading volume

Yahoo Finance data availability depends on market activity

Intraday data is limited to the current trading day

These are expected constraints of public market data APIs.

🧭 Future Improvements

VWAP indicator

Market session separators (open / close markers)

Price & volume alerts

Multi-stock comparison view

Mobile-first layout optimizations

🧑‍💻 Author

Built by Varun Reddy Patel
Designed as a portfolio project demonstrating real-time data handling, visualization, and cloud deployment best practices.

⭐ If You’re Reviewing This Repo

This project intentionally focuses on:

Clean architecture

Practical deployment constraints

Real-world data issues

Clear, readable visualizations

Feedback and suggestions are welcome.