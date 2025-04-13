# indicators/ma.py

import pandas as pd

# ✅ 단순 이동 평균 (SMA) 계산 함수
def calculate_sma(df: pd.DataFrame, period: int = 30) -> pd.Series:
    """
    종가(close)를 기준으로 SMA 계산
    """
    return df["close"].rolling(window=period).mean()

# ✅ MA30 상향/하향 돌파 판단 함수
def detect_ma_crossover(df: pd.DataFrame) -> str | None:
    """
    최근 2개의 캔들에서 MA30 돌파 여부 판단
    - 상향 돌파 (bullish)
    - 하향 돌파 (bearish)
    - 아니면 None
    """
    if len(df) < 2 or "sma" not in df.columns:
        return None

    prev_close = df["close"].iloc[-2]
    curr_close = df["close"].iloc[-1]
    prev_ma = df["sma"].iloc[-2]
    curr_ma = df["sma"].iloc[-1]

    if prev_close < prev_ma and curr_close > curr_ma:
        return "bullish"
    elif prev_close > prev_ma and curr_close < curr_ma:
        return "bearish"
    return None