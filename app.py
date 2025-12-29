import streamlit as st
import pandas as pd
import yfinance as yf
from time import sleep

from core.screener import swing_screen
from core.sentiment import composite_sentiment

st.set_page_config(layout="wide", page_title="Quant Swing Screener")
st.title("📈 Quant Swing Trading Screener (1–3 Months)")
st.caption("Trend intact • Momentum reset • Institutional bias")

tab1, tab2 = st.tabs(["📊 Screener", "🔍 Detailed Analysis"])

# -------------------- FUNCTIONS --------------------
@st.cache_data(ttl=86400)
def get_nse_stock_list():
    """Fetch the official list of all NSE equities and convert to `.NS` tickers."""
    try:
        url = "https://www.nseindia.com/static/market-data/SE_FNDIAEQ.csv"
        df = pd.read_csv(url)
        tickers = df["SYMBOL"].dropna().unique().tolist()
        return [t + ".NS" for t in tickers]
    except Exception as e:
        st.error("Error fetching NSE company list — using fallback list.")
        return []

def load_price_data(ticker):
    """Download price data using yfinance with MultiIndex mitigation."""
    df = yf.download(ticker, period="2y", interval="1d", progress=False)
    # flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join([str(c) for c in col]).strip() for col in df.columns]
    # ensure Close exists
    if "Close" not in df.columns and "Adj Close" in df.columns:
        df["Close"] = df["Adj Close"]
    return df

# -------------------- TAB 1: SCREENER --------------------
with tab1:
    st.subheader("🎯 Swing Trade Opportunities (All NSE Stocks)")

    tickers = get_nse_stock_list()
    if not tickers:
        st.stop()

    results = []
    failed_tickers = []

    progress_text = st.empty()
    progress_bar = st.progress(0)

    total = len(tickers)
    for i, ticker in enumerate(tickers):
        progress_text.text(f"Scanning {ticker} ({i+1}/{total})")
        try:
            df = load_price_data(ticker)
            res = swing_screen(df)
            if res and res.get("SwingScore", 0) >= 60:
                results.append({"Stock": ticker, **res})
        except Exception:
            failed_tickers.append(ticker)
        progress_bar.progress((i + 1) / total)
        sleep(0.02)

    if not results:
        st.info("No swing opportunities currently.")
        st.stop()

    screen_df = pd.DataFrame(results).sort_values("SwingScore", ascending=False)

    def color_score(val):
        if val >= 80:
            return "background-color:#1b5e20;color:white"
        elif val >= 65:
            return "background-color:#2e7d32;color:white"
        else:
            return "background-color:#f9a825;color:black"

    st.dataframe(
        screen_df.style.applymap(color_score, subset=["SwingScore"]),
        use_container_width=True
    )

    selected_stock = st.selectbox(
        "Select stock for detailed analysis",
        screen_df["Stock"].unique()
    )

# -------------------- TAB 2: DETAILED ANALYSIS --------------------
with tab2:
    if not selected_stock:
        st.info("Select a stock from Screener tab.")
        st.stop()

    df = load_price_data(selected_stock)
    metrics = swing_screen(df)

    if df is None or df.empty or not metrics:
        st.warning("Data unavailable for this stock.")
        st.stop()

    # Calculate SMAs safely
    if "Close" in df.columns:
        df["SMA50"] = df["Close"].rolling(50).mean()
        df["SMA200"] = df["Close"].rolling(200).mean()

    # Extract metrics
    swing_score = metrics.get("SwingScore")
    rsi = metrics.get("RSI")
    atr_pct = metrics.get("ATR_pct")
    close_val = df["Close"].iloc[-1] if "Close" in df.columns else None
    sma50_val = df["SMA50"].iloc[-1] if "SMA50" in df.columns else None
    sma200_val = df["SMA200"].iloc[-1] if "SMA200" in df.columns else None

    # Composite sentiment
    sent_score, sent_label = composite_sentiment(selected_stock)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Swing Score", swing_score)
    with col2:
        st.metric("Sentiment", sent_label, sent_score)
    with col3:
        st.metric("RSI", rsi)

    st.subheader("📊 Price Trend with Key Averages")

    plot_columns = [col for col in ["Close", "SMA50", "SMA200"] if col in df.columns]
    if plot_columns:
        plot_df = df[plot_columns].dropna()
        if not plot_df.empty:
            st.line_chart(plot_df)
        else:
            st.warning("Not enough data to plot SMA50/200 for this stock.")
    else:
        st.warning("No valid plot columns for this stock.")

    st.subheader("📌 Key Technical Metrics")
    st.write(f"ATR %: {atr_pct}")
    st.write(f"Last Close: {close_val}")
    st.write(f"SMA50: {sma50_val}")
    st.write(f"SMA200: {sma200_val}")

    if failed_tickers:
        st.info(f"⚠ Skipped tickers due to data issues: {len(failed_tickers)}")
