# utils/io/candle_loader.py

import os
import pandas as pd

BASE_PATH = "data/price"

def load_candle_csv(symbol: str, market: str, timeframe: str) -> pd.DataFrame | None:
    """
    저장된 CSV 캔들 데이터를 불러옵니다.
    Returns None if not found or error.
    """
    path = os.path.join(BASE_PATH, market, timeframe, f"{symbol}.csv")

    if not os.path.exists(path):
        print(f"[❌ CSV 없음] {symbol.upper()} ({market}) - {timeframe}")
        return None

    try:
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        return df
    except Exception as e:
        print(f"[⚠️ CSV 로딩 오류] {symbol.upper()} - {e}")
        return None