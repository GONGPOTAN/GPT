import os
import pandas as pd

def get_latest_price(symbol: str, market: str, timeframe: str = "M1") -> float | None:
    """
    가장 최근 CSV 파일에서 종가(close) 정보를 가져옴.
    오류 발생 시 None 반환.
    예: symbol='futures-btcusdt' → 파일명은 'btcusdt.csv'
    """
    # ✅ symbol 에 market 접두사 붙어 있는 경우 제거
    if "-" in symbol:
        _, symbol = symbol.split("-", 1)

    path = f"data/price/{market}/{timeframe}/{symbol.lower()}.csv"

    # ✅ 경로 존재 확인
    if not os.path.exists(path):
        print(f"[get_latest_price] ❌ 파일 없음: {path}")
        return None

    try:
        df = pd.read_csv(path)

        # ✅ 컬럼 존재 여부 확인
        if "close" not in df.columns:
            print(f"[get_latest_price] ❌ 'close' 컬럼 없음: {path}")
            return None

        if df.empty:
            print(f"[get_latest_price] ❌ 데이터프레임 비어 있음: {path}")
            return None

        # ✅ 마지막 종가 가져오기
        latest_close = df.iloc[-1]["close"]
        print(f"[get_latest_price] ✅ {symbol} @ {timeframe} = {latest_close}")
        return float(latest_close)

    except Exception as e:
        print(f"[get_latest_price 예외] {symbol} @ {market}/{timeframe} → {e}")
        return None