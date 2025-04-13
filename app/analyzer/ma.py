import pandas as pd

def analyze_ma(df: pd.DataFrame) -> dict:
    result = {}
    if len(df) < 99 or "close" not in df.columns:
        return result

    closes = df["close"]
    result["ma7"] = closes.rolling(window=7).mean()
    result["ma30"] = closes.rolling(window=30).mean()
    result["ma99"] = closes.rolling(window=99).mean()
    return result
