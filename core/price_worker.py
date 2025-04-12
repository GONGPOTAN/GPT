# core/price_worker.py

from core.state import status_cache
from utils.data_loader import get_latest_price
from config.symbols import all_symbols  # 전체 종목 리스트
import asyncio

# ✅ 실시간 가격을 status_cache 에 반영하는 워커
async def price_worker():
    while True:
        for symbol in all_symbols:
            try:
                latest_price = get_latest_price(symbol, "M1")  # M1 기준 최신 가격 조회
                if latest_price is not None:
                    status_cache[symbol]["price"] = latest_price
            except Exception as e:
                print(f"[price_worker] {symbol} 가격 갱신 실패: {e}")
        await asyncio.sleep(5)  # 5초마다 전체 종목 갱신
