# 📊 Multi Crypto Dashboard | داشبورد کریپتو چندارزی

A Streamlit dashboard that displays multiple cryptocurrencies with key technical indicators like SMA, EMA, Bollinger Bands, RSI, and MACD.  
It allows users to visualize candlestick charts and indicator trends for better market analysis.

یک داشبورد کریپتو با استفاده از Streamlit که قیمت چند ارز دیجیتال را همراه با اندیکاتورهای مهم تکنیکال (SMA، EMA، باند بولینگر، RSI و MACD) نمایش می‌دهد.  
کاربر می‌تواند نمودار کندل‌استیک و روند شاخص‌ها را مشاهده کند و تحلیل بهتری از بازار داشته باشد.

---

## 🧠 Technologies Used | تکنولوژی‌های استفاده‌شده

- Python 3.10+  
- Streamlit (ساخت رابط کاربری وب تعاملی)  
- requests / pandas (دریافت و پردازش داده)  
- Plotly (نمودارهای تعاملی)  

---

## ⚙️ How It Works | نحوه کار

1. Fetch hourly cryptocurrency data from CryptoCompare API.  
   دریافت داده‌های ساعتی ارزهای دیجیتال از CryptoCompare API.

2. Calculate technical indicators:  
   محاسبه اندیکاتورهای تکنیکال:  
   - SMA & EMA  
   - Bollinger Bands  
   - RSI  
   - MACD

3. Display interactive charts for each coin using Plotly and Streamlit.  
   نمایش نمودارهای تعاملی برای هر ارز با استفاده از Plotly و Streamlit.

---

## 🧩 Key Code Structure | ساختار اصلی کد

```python
# Fetch cryptocurrency data
def get_candles(symbol="BTC", limit=200):
    df = pd.DataFrame(requests.get(...).json()["Data"]["Data"])
    df["time"] = pd.to_datetime(df["time"], unit="s")

    # Calculate SMA & EMA
    df["SMA20"] = df["c"].rolling(20).mean()
    df["EMA50"] = df["c"].ewm(span=50, adjust=False).mean()

    # Bollinger Bands
    df["BB_upper"] = df["c"].rolling(20).mean() + 2 * df["c"].rolling(20).std()
    df["BB_lower"] = df["c"].rolling(20).mean() - 2 * df["c"].rolling(20).std()

    # RSI
    delta = df["c"].diff()
    gain = delta.where(delta>0,0)
    loss = -delta.where(delta<0,0)
    df["RSI"] = 100 - (100/(1 + gain.rolling(14).mean()/loss.rolling(14).mean()))

    # MACD
    ema12 = df["c"].ewm(span=12, adjust=False).mean()
    ema26 = df["c"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

# Display charts for each coin
for coin in ["BTC","ETH","BNB"]:
    df = get_candles(coin)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df["time"], open=df["o"], high=df["h"], low=df["l"], close=df["c"]))
    fig.add_trace(go.Scatter(x=df["time"], y=df["SMA20"], name="SMA20"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["EMA50"], name="EMA50"))
    st.plotly_chart(fig, use_container_width=True)
