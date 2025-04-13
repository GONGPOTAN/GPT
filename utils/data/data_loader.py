# utils/data/data_loader.py

import os
import pandas as pd

BASE_PATH = "data/price"

def get_latest_price(symbol: str, market: str, timeframe: str = "M1") -> float | None:
    """
    종목 CSV에서 마지막 close 값을 반환합니다.
    """
    # 'futures-btcusdt' → 'btcusdt'
    if "-" in symbol:
        _, symbol = symbol.split("-", 1)

    path = os.path.join(BASE_PATH, market, timeframe, f"{symbol.lower()}.csv")

    if not os.path.exists(path):
        print(f"[❌ 파일 없음] {symbol.upper()} ({market}/{timeframe}) → {path}")
        return None

    try:
        df = pd.read_csv(path)

        if df.empty:
            print(f"[⚠️ 빈 CSV] {symbol.upper()} → {path}")
            return None

        if "close" not in df.columns:
            print(f"[❌ 'close' 없음] {symbol.upper()} → {path}")
            return None

        latest = float(df.iloc[-1]["close"])
        print(f"[✅ 최신 종가] {symbol.upper()} → {latest}")
        return latest

    except Exception as e:
        print(f"[❌ 예외] {symbol.upper()} → {e}")
        return None