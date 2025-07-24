import streamlit as st
import pandas as pd
from lbank_connector_python import Client  # 수정된 임포트

API_KEY = "ccc758a1-fe95-4e2d-8be3-581844cbee21"
SECRET_KEY = "4D364D019AD6C305DFFCCCEA19BE412C"

client = Client(api_key=API_KEY, secret_key=SECRET_KEY)

def fetch_lbank_data():
    try:
        result = client.get_contract_ticker("btc_usdt")
        data = [{
            "symbol": "BTC/USDT",
            "price": float(result['last_price']),
            "volume": float(result['volume'])
        }]
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"API 호출 실패: {e}")
        # 임시 예시 데이터 반환
        data = {
            'symbol': ['BTC/USDT'],
            'price': [30000],
            'volume': [10000]
        }
        return pd.DataFrame(data)

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
    if pd.isna(ma) or pd.isna(rsi):
        return "HOLD"
    if price > ma and rsi < 70:
        return 'LONG'
    elif price < ma and rsi > 30:
        return 'SHORT'
    else:
        return 'HOLD'

st.title("LBank BTC/USDT 실시간 타점 신호 (수정 완료)")

df = fetch_lbank_data()

st.write("### 현재 시세")
st.dataframe(df)

df['MA20'] = calculate_ma(df['price'])
df['RSI14'] = calculate_rsi(df['price'])

df['Signal'] = df.apply(lambda row: generate_signal(row['price'], row['MA20'], row['RSI14']), axis=1)

st.write("### 타점 신호")
st.dataframe(df[['symbol', 'price', 'MA20', 'RSI14', 'Signal']])
