# core/workers/price_worker.py

import asyncio
from config.symbols import get_all_symbols
from utils.data_loader import get_latest_price
from core.state.status_cache import update_price

SLEEP_INTERVAL = 5
TIMEFRAME = "M1"

async def price_worker():
    print("[📡 가격 워커] 시작됨 - 실시간 가격 갱신 중...")

    symbols_by_market = get_all_symbols()

    while True:
        for market, symbol_list in symbols_by_market.items():
            for symbol in symbol_list:
                await fetch_and_update_price(market, symbol)
        await asyncio.sleep(SLEEP_INTERVAL)

async def fetch_and_update_price(market: str, symbol: str):
    try:
        latest_price = get_latest_price(symbol, market, TIMEFRAME)
        if latest_price is not None:
            update_price(symbol, market, latest_price)
            print(f"[✅ 가격 업데이트] {market.upper()}-{symbol.upper()} → {latest_price}")
        else:
            print(f"[⚠️ 가격 없음] {market}-{symbol} → None")
    except Exception as e:
        print(f"[❌ 가격 오류] {market}-{symbol} 갱신 실패: {e}")