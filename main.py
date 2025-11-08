import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Multi Crypto Dashboard", layout="wide")
st.title("📊 داشبورد کریپتو با اندیکاتورها برای چند ارز")

# لیست ارزها
coins = ["BTC", "ETH", "BNB", "SOL", "ADA"]

# گرفتن داده کندل‌ها
def get_candles(symbol="BTC", limit=200):
    url = "https://min-api.cryptocompare.com/data/v2/histohour"
    params = {"fsym": symbol, "tsym": "USD", "limit": limit}
    r = requests.get(url, params=params).json()
    data = r["Data"]["Data"]
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df.rename(columns={"open":"o", "high":"h", "low":"l", "close":"c"}, inplace=True)

    # SMA & EMA
    df["SMA20"] = df["c"].rolling(20).mean()
    df["EMA50"] = df["c"].ewm(span=50, adjust=False).mean()

    # Bollinger Bands
    df["BB_mid"] = df["c"].rolling(20).mean()
    df["BB_std"] = df["c"].rolling(20).std()
    df["BB_upper"] = df["BB_mid"] + (2 * df["BB_std"])
    df["BB_lower"] = df["BB_mid"] - (2 * df["BB_std"])

    # RSI
    delta = df["c"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["c"].ewm(span=12, adjust=False).mean()
    ema26 = df["c"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

# نمایش برای همه ارزها
for coin in coins:
    st.subheader(f"💎 {coin}/USD")

    df = get_candles(coin)

    # ---- نمودار اصلی (کندل + SMA + EMA + باند بولینگر)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df["time"], open=df["o"], high=df["h"],
                                 low=df["l"], close=df["c"], name="Candles"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["SMA20"], mode="lines", name="SMA20"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["EMA50"], mode="lines", name="EMA50"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["BB_upper"], line=dict(width=1, color="gray"), name="BB Upper"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["BB_lower"], line=dict(width=1, color="gray"), name="BB Lower"))
    fig.update_layout(title=f"{coin} with Indicators", xaxis_rangeslider_visible=False, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # ---- RSI
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df["time"], y=df["RSI"], mode="lines", name="RSI"))
    fig_rsi.add_hline(y=70, line_dash="dot", line_color="red")
    fig_rsi.add_hline(y=30, line_dash="dot", line_color="green")
    fig_rsi.update_layout(title=f"{coin} - RSI", height=250)
    st.plotly_chart(fig_rsi, use_container_width=True)

    # ---- MACD
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df["time"], y=df["MACD"], mode="lines", name="MACD"))
    fig_macd.add_trace(go.Scatter(x=df["time"], y=df["Signal"], mode="lines", name="Signal"))
    fig_macd.update_layout(title=f"{coin} - MACD", height=250)
    st.plotly_chart(fig_macd, use_container_width=True)

    st.markdown("---")