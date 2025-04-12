# core/price_worker.py

import asyncio
from config.symbols import get_all_symbols
from utils.data_loader import get_latest_price
from core.status_cache import update_price

# ✅ 실시간 가격을 status_cache 에 반영하는 워커
async def price_worker():
    print("[📈 가격 워커] 시작됨 - 실시간 가격 갱신 중...")
    while True:
        try:
            symbols_by_market = get_all_symbols()
            for market, symbol_list in symbols_by_market.items():
                for symbol in symbol_list:
                    try:
                        latest_price = get_latest_price(symbol, market, "M1")
                        if latest_price is not None:
                            update_price(symbol, market, latest_price)
                            print(f"[📈 가격 업데이트] {market.upper()}-{symbol.upper()} → {latest_price}")
                    except Exception as e:
                        print(f"[❌ 가격 오류] {market}-{symbol} 갱신 실패: {e}")
        except Exception as e:
            print(f"[❌ 심각] 전체 종목 처리 중 예외 발생: {e}")
        
        await asyncio.sleep(5)