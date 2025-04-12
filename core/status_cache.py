# core/status_cache.py

from collections import defaultdict
from datetime import datetime
import threading

# ✅ 스레드 안전을 위한 Lock 사용
_cache_lock = threading.Lock()

# ✅ 종목 상태 캐시: { "futures-btcusdt": {...}, "spot-ethusdt": {...} }
status_cache = defaultdict(lambda: {
    "price": None,           # 실시간 가격
    "rsi": {},               # RSI 정보 (timeframe 별)
    "trend": {},             # 추세 정보 (timeframe 별)
    "updated_at": None       # 마지막 갱신 시각 (UTC 기준)
})

# ✅ 가격 업데이트 함수
def update_price(symbol: str, market: str, price: float):
    key = f"{market}-{symbol.lower()}"
    with _cache_lock:
        status_cache[key]["price"] = price
        status_cache[key]["updated_at"] = datetime.utcnow()

# ✅ RSI 업데이트 함수
def update_rsi(symbol: str, market: str, timeframe: str, value: float):
    key = f"{market}-{symbol.lower()}"
    with _cache_lock:
        status_cache[key]["rsi"][timeframe] = value
        status_cache[key]["updated_at"] = datetime.utcnow()

# ✅ 추세 업데이트 함수
def update_trend(symbol: str, market: str, timeframe: str, trend_str: str):
    key = f"{market}-{symbol.lower()}"
    with _cache_lock:
        status_cache[key]["trend"][timeframe] = trend_str
        status_cache[key]["updated_at"] = datetime.utcnow()

# ✅ FastAPI에서 참조할 전체 상태 반환 함수
def get_all_status():
    with _cache_lock:
        # FastAPI가 JSON 직렬화 가능한 구조로 변환
        return dict(status_cache)