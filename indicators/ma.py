# indicators/ma.py

import pandas as pd

def calculate_sma(series: pd.Series, period: int = 30) -> pd.Series:
    return series.rolling(window=period).mean()