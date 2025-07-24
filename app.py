import streamlit as st
import requests
import pandas as pd
import numpy as np

# 이동평균 계산
def calculate_ma(prices, window=20):
    return prices.rolling(window=window).mean()

# RSI 계산
def calculate_rsi(prices, window=14):
    delta = prices.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=window).mean()
    ma_down = down.rolling(window=window).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

# LBank 선물 상위종목 실시간 API 호출 (예시)
def get_lbank_data():
    url = 'https://api.lbank.info/api/v1/ticker.do?symbol=btc_usdt'  # BTC/USDT 단일 심볼 예시
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        price = float(data['ticker']['latest'])
        volume = float(data['ticker']['vol'])
        df = pd.DataFrame([{'symbol': 'BTC/USDT', 'price': price, 'volume': volume}])
        return df
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        # 임시 데이터로 대체
        return pd.DataFrame({
            'symbol': ['BTC/USDT', 'ETH/USDT', 'XRP/USDT'],
            'price': [30000, 2000, 0.5],
            'volume': [10000, 5000, 2000]
        })

def generate_signal(price, ma, rsi):
    if price > ma and rsi < 70:
        return 'LONG'
    elif price < ma and rsi > 30:
        return 'SHORT'
    else:
        return 'HOLD'

st.title("LBank 선물 실시간 타점 신호")

df = get_lbank_data()

st.write("### 현재 주요 종목 시세")
st.dataframe(df)

df['MA20'] = calculate_ma(df['price'])
df['RSI14'] = calculate_rsi(df['price'])

df['Signal'] = df.apply(lambda row: generate_signal(row['price'], row['MA20'], row['RSI14']), axis=1)

st.write("### 타점 신호")
st.dataframe(df[['symbol', 'price', 'MA20', 'RSI14', 'Signal']])

st.write("**참고**: API 호출 실패 시 임시 데이터로 대체합니다.")
