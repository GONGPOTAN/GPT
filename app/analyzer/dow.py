import pandas as pd

def analyze_dow(df: pd.DataFrame, lookback: int = 20) -> dict:
    if len(df) < lookback or not {"high", "low"}.issubset(df.columns):
        return {}

    highs = df["high"].tail(lookback)
    lows = df["low"].tail(lookback)

    recent_highs = highs[highs > highs.shift(1)]
    recent_lows = lows[lows < lows.shift(1)]

    is_uptrend = recent_highs.is_monotonic_increasing and recent_lows.is_monotonic_increasing
    is_downtrend = recent_highs.is_monotonic_decreasing and recent_lows.is_monotonic_decreasing

    if is_uptrend:
        trend = "상승추세"
    elif is_downtrend:
        trend = "하락추세"
    else:
        trend = "횡보"

    return {"trend": trend}
