import streamlit as st
import pandas as pd

from data.loader import get_nse_stock_list, load_price_data
from core.screener import swing_screen
from core.sentiment import composite_sentiment

st.set_page_config(layout="wide", page_title="Quant Swing Screener")

st.title("📈 Quant Swing Trading Screener (1–3 Months)")
st.caption("Trend intact • Momentum reset • Institutional bias")

tab1, tab2 = st.tabs(["📊 Screener", "🔍 Detailed Analysis"])

# -------------------- TAB 1: SCREENER --------------------
with tab1:
    st.subheader("🎯 Swing Trade Opportunities (All NSE Stocks)")

    tickers = get_nse_stock_list()
    results = []
    failed_tickers = []

    progress_text = st.empty()
    progress_bar = st.progress(0)

    for i, ticker in enumerate(tickers[:300]):  # limit to first 300 for free tier
        progress_text.text(f"Scanning {ticker} ({i+1}/{len(tickers[:300])})")
        try:
            df = load_price_data(ticker)
            res = swing_screen(df)
            if res and res["SwingScore"] >= 60:
                results.append({"Stock": ticker, **res})
        except Exception as e:
            failed_tickers.append(ticker)
            continue
        progress_bar.progress((i + 1) / 300)

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

    # Force Close column
    if "Close" not in df.columns and "Adj Close" in df.columns:
        df["Close"] = df["Adj Close"]

    # Compute SMAs safely
    df["SMA50"] = df["Close"].rolling(50).mean()
    df["SMA200"] = df["Close"].rolling(200).mean()

    # Metrics display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Swing Score", metrics["SwingScore"])
    with col2:
        sent_score, sent_label
