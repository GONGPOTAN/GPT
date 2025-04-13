import requests
from collections import defaultdict, deque
from datetime import datetime

class PriceFetcher:
    BASE_URL_SPOT = "https://api.binance.com"
    BASE_URL_FUTURES = "https://fapi.binance.com"

    # Recommended number of candles to keep for each interval
    MAX_CANDLE_COUNTS = {
        "1m": 1000,
        "15m": 500,
        "1h": 400,
        "4h": 300,
        "1d": 180,
        "1w": 60,
    }

    def __init__(self):
        self._cache = defaultdict(lambda: defaultdict(lambda: deque(maxlen=0)))  # market -> symbol -> deque

    def fetch(self, symbol: str, interval: str, limit: int = 500, market: str = "futures", start_time: int = None) -> list:
        if market == "spot":
            base_url = self.BASE_URL_SPOT
        elif market == "futures":
            base_url = self.BASE_URL_FUTURES
        else:
            raise ValueError(f"Unsupported market type: {market}")

        endpoint = "/api/v3/klines" if market == "spot" else "/fapi/v1/klines"
        url = f"{base_url}{endpoint}"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        if start_time:
            params["startTime"] = start_time

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # Initialize deque with maxlen if not already done
        maxlen = self.MAX_CANDLE_COUNTS.get(interval, 500)
        symbol_cache = self._cache[market][symbol]
        if symbol_cache.maxlen != maxlen:
            self._cache[market][symbol] = deque(maxlen=maxlen)
            symbol_cache = self._cache[market][symbol]

        # Extend and auto-trim to maxlen
        symbol_cache.extend(data)
        return list(symbol_cache)

def should_update(interval: str, now: datetime) -> bool:
    if interval == "1m":
        return True
    elif interval == "15m":
        return now.minute % 15 == 0 and now.second == 0
    elif interval == "1h":
        return now.minute == 0 and now.second == 0
    elif interval == "4h":
        return now.hour % 4 == 0 and now.minute == 0 and now.second == 0
    elif interval == "1d":
        return now.hour == 0 and now.minute == 0 and now.second == 0
    elif interval == "1w":
        return now.weekday() == 0 and now.hour == 0 and now.minute == 0 and now.second == 0
    return False
