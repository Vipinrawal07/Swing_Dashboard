import yfinance as yf
import pandas as pd
import streamlit as st

@st.cache_data(ttl=86400)
def get_nse_stock_list():
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    df = pd.read_csv(url)
    return (df["SYMBOL"] + ".NS").tolist()


@st.cache_data(ttl=3600)
def load_price_data(ticker):
    try:
        df = yf.download(ticker, period="2y", interval="1d", progress=False)
        return df if not df.empty else None
    except:
        return None
