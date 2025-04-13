# indicators/dow_theory.py

import pandas as pd

def detect_dow_trend(df: pd.DataFrame) -> str:
    if len(df) < 3:
        return "UNKNOWN"

    last_high = df["high"].iloc[-2]
    current_high = df["high"].iloc[-1]
    last_low = df["low"].iloc[-2]
    current_low = df["low"].iloc[-1]

    if current_high > last_high and current_low > last_low:
        return "HH-HL"
    elif current_high < last_high and current_low < last_low:
        return "LL-LH"
    elif current_high > last_high and current_low < last_low:
        return "확장형"
    else:
        return "중립"