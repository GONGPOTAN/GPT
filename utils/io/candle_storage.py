# utils/io/candle_storage.py

import os
import pandas as pd

BASE_PATH = "data/price"

def save_candle(symbol: str, market: str, timeframe: str, df: pd.DataFrame, max_rows: int = 3000):
    """
    캔들 데이터 저장 (CSV 병합 및 정렬, 중복 제거 포함)
    """
    if df.empty:
        print(f"[📂 저장 생략] {symbol.upper()} ({market}) {timeframe} → 데이터 없음")
        return

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    save_dir = os.path.join(BASE_PATH, market, timeframe)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, f"{symbol}.csv")

    try:
        if os.path.exists(file_path):
            old_df = pd.read_csv(file_path)
            old_df["timestamp"] = pd.to_datetime(old_df["timestamp"])
            df = pd.concat([old_df, df], ignore_index=True)

        df = (
            df.drop_duplicates(subset="timestamp")
              .sort_values("timestamp")
              .tail(max_rows)
        )

        df.to_csv(file_path, index=False)
        print(f"[💾 저장 완료] {symbol.upper()} ({market}) {timeframe} → {len(df)} rows")

    except Exception as e:
        print(f"[❌ 저장 오류] {symbol.upper()} → {e}")