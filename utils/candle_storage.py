# utils/candle_storage.py

import os
import pandas as pd

def save_candle(symbol: str, market: str, timeframe: str, df: pd.DataFrame, max_rows: int = 3000):
    """
    CSV 파일로 캔들 데이터를 저장하는 함수
    - 기존 데이터와 병합하여 최대 max_rows 까지만 저장
    - 중복 timestamp 제거 및 시간 정렬 포함
    - 파일 경로: data/price/{market}/{timeframe}/{symbol}.csv
    """

    if df.empty:
        print(f"[CSV 저장 생략] {symbol.upper()} ({market}) - {timeframe} 데이터 없음")
        return

    # ✅ timestamp를 datetime으로 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 저장 경로 설정
    base_dir = f"data/price/{market}/{timeframe}"
    os.makedirs(base_dir, exist_ok=True)
    filepath = os.path.join(base_dir, f"{symbol}.csv")

    # 기존 데이터 병합
    if os.path.exists(filepath):
        try:
            existing = pd.read_csv(filepath)
            existing['timestamp'] = pd.to_datetime(existing['timestamp'])
            df = pd.concat([existing, df], ignore_index=True)
        except Exception as e:
            print(f"[CSV 병합 오류] {symbol.upper()} - {e}")

    # ✅ 중복 제거 및 시간순 정렬
    df = df.drop_duplicates(subset='timestamp', keep='last')
    df = df.sort_values(by='timestamp')

    # ✅ max_rows 초과 시 오래된 것 제거
    if len(df) > max_rows:
        df = df.iloc[-max_rows:]

    # 저장
    try:
        df.to_csv(filepath, index=False)
    except Exception as e:
        print(f"[CSV 저장 오류] {symbol.upper()} - {e}")