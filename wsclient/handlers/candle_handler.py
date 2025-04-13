# wsclient/handlers/candle_handler.py
import json
import pandas as pd
from datetime import datetime
from core.status_cache import update_price
from utils.io.candle_storage import save_candle

from config.symbols import get_all_symbols

price_cache = {}

def get_market_type(symbol: str) -> str:
    all_symbols = get_all_symbols()
    if symbol in [s.lower() for s in all_symbols["futures"]]:
        return "futures"
    return "spot"

async def handle_candle(message: str):
    data = json.loads(message)
    if 'data' not in data or 'k' not in data['data']:
        return

    k = data['data']['k']
    symbol = data['data']['s'].lower()
    market_type = get_market_type(symbol)

    row = {
        "timestamp": datetime.fromtimestamp(k['t'] / 1000),
        "open": float(k['o']),
        "high": float(k['h']),
        "low": float(k['l']),
        "close": float(k['c']),
        "volume": float(k['v']),
    }

    key = f"{market_type}-{symbol}"
    price_cache.setdefault(key, []).append(row)

    if len(price_cache[key]) > 30:
        price_cache[key] = price_cache[key][-30:]

    df = pd.DataFrame(price_cache[key])
    save_candle(symbol, market_type, "M1", df, max_rows=3000)
    update_price(symbol, market_type, float(k['c']))