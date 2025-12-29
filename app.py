import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

import config
from core.screener import swing_screen
from core.swing_score import swing_score
from core.ui_backtest import run_backtest
from sentiment.sentiment_score import composite_sentiment
from core.helpers import score_color

st.set_page_config("Advisor Swing Dashboard", layout="wide")

# ---------------- STATE ---------------- #
if "selected_stock" not in st.session_state:
    st.session_state.selected_stock = "RELIANCE"

# ---------------- HEADER ---------------- #
st.title("📊 Advisor Swing Trading Dashboard (India)")

tabs = st.tabs(["📊 Screener", "🧪 Backtest", "📌 Signals"])

# ======================================================
# =================== SCREENER TAB =====================
# ======================================================

with tabs[0]:

    # ---------- Sector Selection ----------
    sector = st.selectbox("Select Sector", list(config.SECTORS.keys()))

    stocks = config.SECTORS[sector]

    # ---------- Company Buttons ----------
    cols = st.columns(len(stocks))

    for i, stock in enumerate(stocks):
        df_temp = yf.download(stock + ".NS", period="1y", progress=False)
        index_df = yf.download(config.INDEX_SYMBOL, period="1y", progress=False)

        if len(df_temp) < 200:
            continue

        df_temp = swing_screen(df_temp, index_df)
        sent_temp, _, _, _ = composite_sentiment(stock)
        score_temp = swing_score(df_temp.iloc[-1], sent_temp)

        color = score_color(score_temp)

        if cols[i].button(
            f"{stock} ({score_temp})",
            key=stock
        ):
            st.session_state.selected_stock = stock

        cols[i].markdown(
            f"<div style='height:6px;background:{color}'></div>",
            unsafe_allow_html=True
        )

    # ---------- Load Selected Stock ----------
    stock = st.session_state.selected_stock
    ticker = stock + ".NS"

    df = yf.download(ticker, start=config.START_DATE)
    index_df = yf.download(config.INDEX_SYMBOL, start=config.START_DATE)

    df = swing_screen(df, index_df)
    sent, tw, rd, nw = composite_sentiment(stock)
    latest = df.iloc[-1]
    score = swing_score(latest, sent)

    # ---------- Metrics ----------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Swing Score", score)
    m2.metric("Composite Sentiment", sent)
    m3.metric("RS (30D)", round(latest["RS"], 2))
    m4.metric("RSI", round(latest["RSI"], 1))

    # ---------- Chart ----------
    fig = go.Figure()
    fig.add_candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"]
    )
    fig.add_scatter(x=df.index, y=df["SMA50"], name="SMA50")
    fig.add_scatter(x=df.index, y=df["SMA200"], name="SMA200")

    st.plotly_chart(fig, use_container_width=True)

    # ---------- Advisor Call ----------
    if score >= 75:
        st.success("🟢 ADD / HOLD — High Probability Swing Setup")
    elif score >= 65:
        st.warning("🟡 WATCHLIST — Setup Forming")
    else:
        st.error("🔴 AVOID — Weak Setup")

# ======================================================
# ================= BACKTEST TAB =======================
# ======================================================

with tabs[1]:
    stats = run_backtest(df)
    st.subheader(f"Backtest Results — {stock}")
    st.json(stats)

# ======================================================
# ================= SIGNALS TAB ========================
# ======================================================

with tabs[2]:
    st.subheader(f"Recent Swing Signals — {stock}")
    st.dataframe(
        df[df["Signal"]]
        .tail(15)[["Close", "RSI", "RS"]]
        .round(2),
        use_container_width=True
    )
