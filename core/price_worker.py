# core/price_worker.py

import asyncio
from core.state import status_cache
from utils.data_loader import get_latest_price
from config.symbols import get_all_symbols  # ✅ 함수형으로 변경됨

# ✅ 실시간 가격을 status_cache 에 반영하는 워커
async def price_worker():
    while True:
        all_symbols = get_all_symbols()  # { "spot": [...], "futures": [...] }
        for market, symbols in all_symbols.items():
            for symbol in symbols:
                try:
                    latest_price = get_latest_price(symbol, market, "M1")  # ✅ market 명시
                    if latest_price is not None:
                        if symbol not in status_cache:
                            status_cache[symbol] = {}
                        status_cache[symbol]["price"] = latest_price
                except Exception as e:
                    print(f"[price_worker] {symbol} 가격 갱신 실패: {e}")
        await asyncio.sleep(5)  # 5초마다 전체 종목 갱신