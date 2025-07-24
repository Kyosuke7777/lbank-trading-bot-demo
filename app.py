import streamlit as st
import requests
import pandas as pd

# LBank 선물 시세 API (BTC/USDT 예시)
API_URL = "https://api.lbkex.net/v2/contract/ticker?symbol=BTC_USDT"

def fetch_lbank_price():
    try:
        res = requests.get(API_URL, timeout=5)
        res.raise_for_status()
        data = res.json()
        price = float(data['data']['last'])
        volume = float(data['data']['volume'])
        df = pd.DataFrame([{'symbol': 'BTC/USDT', 'price': price, 'volume': volume}])
        return df
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        return pd.DataFrame()

def calculate_ma(prices, window=20):
    return prices.rolling(window=window).mean()

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=window).mean()
    ma_down = down.rolling(window=window).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def generate_signal(price, ma, rsi):
    if price > ma and rsi < 70:
        return 'LONG'
    elif price < ma and rsi > 30:
        return 'SHORT'
    else:
        return 'HOLD'

st.title("LBank BTC/USDT 실시간 타점 신호")

df = fetch_lbank_price()

if df.empty:
    st.warning("실시간 데이터가 없습니다.")
else:
    st.write("### 현재 BTC/USDT 시세")
    st.dataframe(df)

    df['MA20'] = calculate_ma(df['price'])
    df['RSI14'] = calculate_rsi(df['price'])

    df['Signal'] = df.apply(lambda row: generate_signal(row['price'], row['MA20'], row['RSI14']), axis=1)

    st.write("### 타점 신호")
    st.dataframe(df[['symbol', 'price', 'MA20', 'RSI14', 'Signal']])
