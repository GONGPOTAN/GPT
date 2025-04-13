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
    "volume_signal": None,   # 거래량 시그널 정보 (예: "급등")
    "updated_at": None       # 마지막 갱신 시각 (UTC 기준)
})

volume_spike_cache = []  # 거래량 급등 종목 리스트
signal_event_cache = []  # 최근 시그널 이벤트 리스트

# ✅ 가격 업데이트 함수
def update_price(symbol: str, market: str, price: float):
    key = f"{market}-{symbol.lower()}"
    with _cache_lock:
        status_cache[key]["price"] = float(price)
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

# ✅ 거래량 시그널 업데이트 함수
def update_volume_signal(symbol: str, market: str, signal: str):
    key = f"{market}-{symbol.lower()}"
    with _cache_lock:
        status_cache[key]["volume_signal"] = signal
        status_cache[key]["updated_at"] = datetime.utcnow()

# ✅ FastAPI에서 참조할 전체 상태 반환 함수
def get_all_status():
    with _cache_lock:
        status = dict(status_cache)
        print("[🔍 FastAPI] status_cache 반환:", status)
        return status

# ✅ FastAPI용 단일 종목 가격 반환
def get_price(symbol: str):
    key = symbol.lower()
    with _cache_lock:
        return status_cache.get(key, {}).get("price", None)

# ✅ FastAPI용 RSI 반환
def get_rsi(symbol: str):
    key = symbol.lower()
    with _cache_lock:
        return status_cache.get(key, {}).get("rsi", {})

# ✅ FastAPI용 추세 반환
def get_trend(symbol: str):
    key = symbol.lower()
    with _cache_lock:
        return status_cache.get(key, {}).get("trend", {})

# ✅ FastAPI용 거래량 급등 종목 리스트 반환
def get_volume_spike():
    with _cache_lock:
        return volume_spike_cache.copy()

# ✅ FastAPI용 시그널 이벤트 반환
def get_signal_events():
    with _cache_lock:
        return signal_event_cache.copy()