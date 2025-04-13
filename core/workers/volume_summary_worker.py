# core/workers/volume_summary_worker.py
import asyncio
from datetime import datetime
from config.symbols import get_all_symbols
from indicators.volume import detect_volume_spike
from utils.io.candle_loader import load_candle_csv
from core.state.status_cache import update_volume_signal

INTERVAL = 30

async def volume_summary_worker():
    print("[🔥 거래량 워커] 시작됨 - 급등 탐지")
    symbols_by_market = get_all_symbols()

    while True:
        for market, symbols in symbols_by_market.items():
            for symbol in symbols:
                await analyze_volume(symbol, market)
        await asyncio.sleep(INTERVAL)

async def analyze_volume(symbol: str, market: str):
    try:
        df = load_candle_csv(symbol, market, "M1")
        if df is None or len(df) < 21:
            return
        if detect_volume_spike(df):
            update_volume_signal(symbol, market, True)
            print(f"[📈 거래량 급등] {market}-{symbol}")
    except Exception as e:
        print(f"[❌ 거래량 분석 오류] {market}-{symbol} → {e}")