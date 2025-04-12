# core/price_worker.py

import asyncio
from core.state import status_cache
from utils.data_loader import get_latest_price
from config.symbols import get_all_symbols

# ✅ 전체 종목 구성: futures-btcusdt, spot-ethusdt 형식 등
all_symbols = [
    f"{market}-{symbol}"
    for market, symbols in get_all_symbols().items()
    for symbol in symbols
]

# ✅ 실시간 가격을 status_cache 에 반영하는 워커
async def price_worker():
    print("[📈 가격 워커] 시작됨 - 실시간 가격 갱신 중...")
    while True:
        for symbol in all_symbols:
            try:
                market, base_symbol = symbol.split("-")
                latest_price = get_latest_price(base_symbol, market, "M1")  # 시장 구분 포함
                if latest_price is not None:
                    if symbol not in status_cache:
                        status_cache[symbol] = {}
                    status_cache[symbol]["price"] = latest_price
            except Exception as e:
                print(f"[price_worker] {symbol} 가격 갱신 실패: {e}")
        await asyncio.sleep(5)  # 5초마다 전체 종목 갱신
