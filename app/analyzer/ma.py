import pandas as pd
from config.analysis import ANALYSIS_CONFIG

def analyze_ma(df: pd.DataFrame) -> dict:
    result = {}
    if len(df) < 99 or "close" not in df.columns:
        return result

    closes = df["close"]
    result["ma7"] = closes.rolling(window=ANALYSIS_CONFIG.get("MA7_PERIOD", 7)).mean()
    result["ma30"] = closes.rolling(window=ANALYSIS_CONFIG.get("MA30_PERIOD", 30)).mean()
    result["ma99"] = closes.rolling(window=ANALYSIS_CONFIG.get("MA99_PERIOD", 99)).mean()
    return result
