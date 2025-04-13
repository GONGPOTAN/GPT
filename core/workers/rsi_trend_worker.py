# core/workers/rsi_trend_worker.py

import asyncio
from datetime import datetime
from config.symbols import get_all_symbols
from indicators.rsi import calculate_rsi_sma
from indicators.trend import detect_trend_string
from utils.candle_loader import load_candle_csv
from core.state.status_cache import update_rsi, update_trend

TIMEFRAMES = ["H1", "H4", "D"]
MIN_CANDLES = {"H1": 100, "H4": 100, "D": 100}
INTERVAL = 60

async def rsi_trend_worker():
    print("[📊 RSI/Trend 워커] 시작됨 - 상태 캐시 주기 갱신")
    symbols_by_market = get_all_symbols()

    while True:
        for market, symbols in symbols_by_market.items():
            for symbol in symbols:
                await analyze_symbol(symbol, market)
        await asyncio.sleep(INTERVAL)

async def analyze_symbol(symbol: str, market: str):
    for tf in TIMEFRAMES:
        try:
            df = load_candle_csv(symbol, market, tf)
            if df is None or len(df) < MIN_CANDLES[tf]:
                return

            rsi = calculate_rsi_sma(df["close"])
            if not rsi.empty:
                latest_rsi = rsi.iloc[-1]
                update_rsi(symbol, market, tf, round(latest_rsi, 2))

            trend = detect_trend_string(df)
            if trend:
                update_trend(symbol, market, tf, trend)

            print(f"[{datetime.utcnow()}] {market}-{symbol}({tf}) → RSI: {latest_rsi:.2f}, Trend: {trend}")
        except Exception as e:
            print(f"[⚠️ 분석 오류] {market}-{symbol}({tf}) → {e}")