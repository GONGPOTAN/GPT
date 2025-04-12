# indicators/ma.py

import pandas as pd

def calculate_sma(df: pd.DataFrame, period: int = 30, price_col: str = "close") -> pd.Series:
    """
    주어진 종가 기준으로 SMA(Simple Moving Average)를 계산합니다.
    기본적으로 MA30을 계산하며, 다른 기간도 설정 가능.
    """
    return df[price_col].rolling(window=period, min_periods=period).mean()

def detect_ma_crossover(df: pd.DataFrame, sma_col: str = "sma") -> str:
    """
    캔들 종가가 MA를 상향 또는 하향 돌파했는지 판단합니다.
    최근 2개의 캔들로 비교함.
    반환값: "bullish", "bearish", 또는 None
    """
    if len(df) < 2 or sma_col not in df.columns:
        return None

    prev_close, curr_close = df["close"].iloc[-2], df["close"].iloc[-1]
    prev_sma, curr_sma = df[sma_col].iloc[-2], df[sma_col].iloc[-1]

    # 상향 돌파: 이전엔 아래, 지금은 위
    if prev_close < prev_sma and curr_close > curr_sma:
        return "bullish"
    # 하향 돌파: 이전엔 위, 지금은 아래
    elif prev_close > prev_sma and curr_close < curr_sma:
        return "bearish"
    return None