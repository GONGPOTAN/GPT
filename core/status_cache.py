# core/status_cache.py

from collections import defaultdict
from datetime import datetime

# 종목 상태 캐시 (가격, RSI, 추세, 마지막 업데이트 시각)
status_cache = defaultdict(lambda: {
    "price": None,
    "rsi": {},
    "trend": {},
    "updated_at": None
})

def update_price(symbol: str, market: str, price: float):
    key = f"{market}-{symbol.lower()}"
    status_cache[key]["price"] = price
    status_cache[key]["updated_at"] = datetime.utcnow()

def update_rsi(symbol: str, market: str, timeframe: str, value: float):
    key = f"{market}-{symbol.lower()}"
    status_cache[key]["rsi"][timeframe] = value
    status_cache[key]["updated_at"] = datetime.utcnow()

def update_trend(symbol: str, market: str, timeframe: str, trend_str: str):
    key = f"{market}-{symbol.lower()}"
    status_cache[key]["trend"][timeframe] = trend_str
    status_cache[key]["updated_at"] = datetime.utcnow()

def get_all_status():
    # FastAPI에서 JSON 직렬화 가능하도록 dict 형태로 변환
    return dict(status_cache)