# storage/status_cache/status_cache.py

from datetime import datetime

# 메모리 기반 상태 캐시
status_cache = {}

def get_key(symbol: str, market: str) -> str:
    return f"{market}-{symbol}"

def update_price(symbol: str, market: str, price: float):
    key = get_key(symbol, market)
    if key not in status_cache:
        status_cache[key] = {"price": None, "rsi": {}, "trend": {}, "updated_at": None}
    status_cache[key]["price"] = price
    status_cache[key]["updated_at"] = datetime.utcnow().isoformat()

def update_rsi(symbol: str, market: str, timeframe: str, value: float):
    key = get_key(symbol, market)
    if key not in status_cache:
        status_cache[key] = {"price": None, "rsi": {}, "trend": {}, "updated_at": None}
    status_cache[key]["rsi"][timeframe] = value
    status_cache[key]["updated_at"] = datetime.utcnow().isoformat()

def update_trend(symbol: str, market: str, timeframe: str, value: str):
    key = get_key(symbol, market)
    if key not in status_cache:
        status_cache[key] = {"price": None, "rsi": {}, "trend": {}, "updated_at": None}
    status_cache[key]["trend"][timeframe] = value
    status_cache[key]["updated_at"] = datetime.utcnow().isoformat()