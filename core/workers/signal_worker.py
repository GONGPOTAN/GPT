# core/workers/signal_worker.py

import asyncio
from config.symbols import get_all_symbols
from alert.signal_checker import check_signals
from alert.signal_queue import signal_queue

async def signal_worker():
    print("[🚨 시그널 워커] 시작됨 - 조건 확인 및 큐에 적재")

    while True:
        symbols_by_market = get_all_symbols()
        for market_type, symbols in symbols_by_market.items():
            for symbol in symbols:
                try:
                    await check_signals(symbol, market_type)  # ✅ 인자 전달
                except Exception as e:
                    print(f"[❌ 시그널 워커 오류] {symbol} ({market_type}) → {e}")

        await asyncio.sleep(30)  # or any reasonable interval