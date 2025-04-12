# utils/data_loader.py

import os
import pandas as pd

def get_latest_price(symbol: str, market: str, timeframe: str = "M1") -> float | None:
    """
    가장 최근 CSV 파일의 종가(close)를 불러옴
    """
    path = f"data/price/{market}/{timeframe}/{symbol.lower()}.csv"
    if not os.path.exists(path):
        return None

    try:
        df = pd.read_csv(path)
        if not df.empty:
            return float(df.iloc[-1]["close"])
    except Exception as e:
        print(f"[get_latest_price 오류] {symbol} {market} → {e}")
    return None