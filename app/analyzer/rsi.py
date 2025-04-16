import pandas as pd
from config.analysis import ANALYSIS_CONFIG

def analyze_rsi(df: pd.DataFrame) -> dict:
    period = ANALYSIS_CONFIG.get("RSI_PERIOD", 14)
    if len(df) < period + 1 or "close" not in df.columns:
        return {}

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return {"rsi": rsi.iloc[-1]}
