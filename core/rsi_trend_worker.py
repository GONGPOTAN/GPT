# core/rsi_trend_worker.py

import asyncio
import pandas as pd
from datetime import datetime
from config.symbols import get_all_symbols
from indicators.rsi import calculate_rsi_sma
from indicators.trend import detect_trend_string
from utils.candle_loader import load_candle_csv
from core.status_cache import update_rsi, update_trend

# ✅ 분석 대상 시간대 및 반복 주기 설정
TIMEFRAMES = ["H1", "H4", "D"]
INTERVAL = 60  # 초 단위 반복 주기

# ✅ 각 시간대별 최소 캔들 수 정의
MIN_CANDLES = {
    "H1": 100,
    "H4": 100,
    "D": 100
}

async def rsi_trend_worker():
    print("[📊 RSI/Trend 워커] 시작됨 - 상태 캐시 주기적 갱신")
    while True:
        try:
            symbols = get_all_symbols()
            for market, symbol_list in symbols.items():
                for symbol in symbol_list:
                    for tf in TIMEFRAMES:
                        try:
                            df = load_candle_csv(symbol, market, tf)
                            if df is None or len(df) < MIN_CANDLES[tf]:
                                continue

                            # ✅ RSI 계산
                            rsi = calculate_rsi_sma(df["close"])
                            if not rsi.empty:
                                latest_rsi = rsi.iloc[-1]
                                update_rsi(symbol, market, tf, round(latest_rsi, 2))

                            # ✅ 추세 판단
                            trend_str = detect_trend_string(df)
                            if trend_str:
                                update_trend(symbol, market, tf, trend_str)

                            # ✅ 로그 출력
                            print(f"[{datetime.utcnow()}] {market}-{symbol}({tf}) → RSI: {latest_rsi:.2f}, Trend: {trend_str}")

                        except Exception as inner_e:
                            print(f"[RSI/Trend] ⚠️ {symbol.upper()}({market})-{tf} 처리 오류: {inner_e}")

        except Exception as e:
            print(f"[RSI/Trend 워커 오류] ❌ {e}")

        await asyncio.sleep(INTERVAL)