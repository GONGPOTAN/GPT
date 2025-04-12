# indicators/rsi.py

import pandas as pd

# ✅ RSI 계산 함수 (SMA 기반)
def calculate_rsi_sma(close: pd.Series, period: int = 14) -> pd.Series:
    """
    SMA 기반 RSI 계산 함수 (OKX / TradingView 방식과 일치)
    """
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
