import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

from core.screener import swing_screen
from core.swing_score import swing_score
from core.ui_backtest import run_backtest
from sentiment.sentiment_score import composite_sentiment
import config

st.set_page_config("Advisor Swing Dashboard", layout="wide")

tabs = st.tabs(["📊 Screener", "🧪 Backtest", "📌 Signals"])

asset = st.selectbox(
    "Select Asset",
    ["RELIANCE", "TCS", "INFY", "HDFCBANK", "GOLD", "SILVER"]
)

symbol_map = {"GOLD": "GC=F", "SILVER": "SI=F"}
ticker = symbol_map.get(asset, asset + ".NS")

df = yf.download(ticker, start=config.START_DATE)
index_df = yf.download(config.INDEX_SYMBOL, start=config.START_DATE)

df = swing_screen(df, index_df)
sent, tw, rd, nw = composite_sentiment(asset)
latest = df.iloc[-1]
score = swing_score(latest, sent)

with tabs[0]:
    st.metric("Swing Score", score)
    st.metric("Composite Sentiment", sent)

    fig = go.Figure()
    fig.add_candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"]
    )
    fig.add_scatter(x=df.index, y=df["SMA50"], name="SMA50")
    fig.add_scatter(x=df.index, y=df["SMA200"], name="SMA200")
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    stats = run_backtest(df)
    st.json(stats)

with tabs[2]:
    st.dataframe(df[df["Signal"]].tail(15)[["Close", "RSI", "RS"]])
