import streamlit as st
import requests
import pandas as pd
import time

# 제목
st.title("LBank 선물 실시간 타점 신호")

# LBank API URL (예시)
API_URL = "https://api.lbkex.com/v2/future/tickers"

# 지표 계산 함수 예시 (간단히 예시)
def fetch_data():
    try:
        res = requests.get(API_URL)
        data = res.json()
        return data.get("data", [])
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        return []

def process_data(raw_data):
    df = pd.DataFrame(raw_data)
    # 필터: 거래량 상위 30개
    df = df.sort_values(by="vol", ascending=False).head(30)
    # 필요한 컬럼만
    df = df[["symbol", "last", "vol"]]
    df.columns = ["종목", "현재가", "거래량"]
    return df

# 데이터 갱신 주기 (초)
REFRESH_INTERVAL = 10

placeholder = st.empty()

while True:
    raw_data = fetch_data()
    if raw_data:
        df = process_data(raw_data)
        with placeholder.container():
            st.write(f"업데이트 시각: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            st.dataframe(df)
    time.sleep(REFRESH_INTERVAL)
