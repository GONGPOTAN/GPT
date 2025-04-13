# core/services/binance_api.py

import requests
import pandas as pd

BASE_URLS = {
    "spot": "https://api.binance.com",
    "futures": "https://fapi.binance.com"
}

def get_klines(symbol: str, market_type: str, interval: str = "15m", limit: int = 100) -> pd.DataFrame:
    """
    바이낸스에서 캔들 데이터 조회 (OHLCV)
    """
    market_type = market_type.lower()  # ✅ 소문자 통일 (예외 방지)
    print(f"[📦 Binance 요청] {market_type.upper()} - {symbol.upper()} - {interval}")  # ✅ 로그 추가

    endpoint = "/api/v3/klines" if market_type == "spot" else "/fapi/v1/klines"
    url = f"{BASE_URLS[market_type]}{endpoint}"
    params = {"symbol": symbol.upper(), "interval": interval, "limit": limit}

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
        print(f"[❌ Binance Klines 오류] {symbol.upper()}({interval}) → {e}")
        return pd.DataFrame()

def get_24hr_change(symbol: str, market_type: str) -> float:
    """
    종목의 24시간 변동률(%) 반환
    """
    market_type = market_type.lower()  # ✅ 일관성 유지
    endpoint = "/api/v3/ticker/24hr" if market_type == "spot" else "/fapi/v1/ticker/24hr"
    url = f"{BASE_URLS[market_type]}{endpoint}"

    try:
        response = requests.get(url, params={"symbol": symbol.upper()})
        response.raise_for_status()
        data = response.json()
        return float(data["priceChangePercent"])

    except Exception as e:
        print(f"[⚠️ 변동률 오류] {symbol.upper()} → {e}")
        return 0.0