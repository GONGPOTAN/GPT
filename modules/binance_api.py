# modules/binance_api.py

import requests
import pandas as pd
import time

BASE_URLS = {
    "spot": "https://api.binance.com",
    "futures": "https://fapi.binance.com"
}

def get_klines(symbol: str, market_type: str, interval: str = "15m", limit: int = 100) -> pd.DataFrame:
    """
    지정한 종목의 캔들 데이터를 Binance REST API를 통해 받아옴
    - symbol: 'btcusdt'
    - market_type: 'spot' or 'futures'
    - interval: '15m', '1h', '4h', '1d' 등
    - limit: 최대 캔들 개수
    """
    url = f"{BASE_URLS[market_type]}/api/v3/klines" if market_type == "spot" \
        else f"{BASE_URLS[market_type]}/fapi/v1/klines"

    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_volume", "num_trades",
            "taker_base_vol", "taker_quote_vol", "ignore"
        ])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as e:
        print(f"[Binance API 에러] {symbol} {interval}: {e}")
        return pd.DataFrame()

def get_24hr_change(symbol: str, market_type: str) -> float:
    """
    해당 종목의 24시간 가격 변동률을 퍼센트(%)로 반환
    """
    url = f"{BASE_URLS[market_type]}/api/v3/ticker/24hr" if market_type == "spot" \
        else f"{BASE_URLS[market_type]}/fapi/v1/ticker/24hr"

    try:
        response = requests.get(url, params={"symbol": symbol.upper()})
        response.raise_for_status()
        data = response.json()
        return float(data["priceChangePercent"])
    except Exception as e:
        print(f"[24hr 변동률 에러] {symbol}: {e}")
        return 0.0
