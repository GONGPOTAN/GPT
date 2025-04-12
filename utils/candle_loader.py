# utils/candle_loader.py

import os
import pandas as pd

def load_candle_csv(symbol: str, market: str, timeframe: str) -> pd.DataFrame:
    """
    저장된 CSV 파일에서 캔들 데이터를 불러오는 함수
    - 파일 경로: data/price/{market}/{timeframe}/{symbol}.csv
    - 데이터프레임 정렬 및 타입 변환 수행
    """
    path = f"data/price/{market}/{timeframe}/{symbol}.csv"
    if not os.path.exists(path):
        print(f"[CSV 로딩 실패] {symbol.upper()} ({market}) - {timeframe} 파일 없음")
        return pd.DataFrame()

    try:
        df = pd.read_csv(path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values(by='timestamp')
        return df
    except Exception as e:
        print(f"[CSV 로딩 오류] {symbol.upper()} - {e}")
        return pd.DataFrame()


# indicators/rsi.py (추가)
import pandas as pd
import numpy as np

def calculate_rsi_sma(close: pd.Series, period: int = 14) -> pd.Series:
    """
    SMA 기반 RSI 계산 함수 (OKX와 동일 방식)
    """
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# indicators/trend.py (추가)
def detect_trend_string(df: pd.DataFrame) -> str:
    """
    다우이론 기반 추세 문자열 반환
    - 최근 3개의 고가/저가를 기준으로 LL→HL 등 판단
    - 최소 3개 이상 데이터 필요
    """
    if len(df) < 3:
        return "-"

    lows = df['low'].iloc[-3:]
    highs = df['high'].iloc[-3:]

    prev_ll, prev_lh = lows.iloc[0], highs.iloc[0]
    curr_ll, curr_lh = lows.iloc[-1], highs.iloc[-1]

    if curr_ll > prev_ll and curr_lh > prev_lh:
        return "상승 전환 (LL → HL)"
    elif curr_ll < prev_ll and curr_lh < prev_lh:
        return "하락 전환 (HH → LH)"
    else:
        return "추세 유지"
