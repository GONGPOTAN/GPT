# wsclient/binance_ws.py

import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime
from collections import defaultdict
from config.symbols import get_all_symbols
from core.signal_queue import signal_queue
from core.volume_summary_worker import volume_ongoing_pool
from core.status_cache import update_price  # ✅ 실시간 가격 업데이트
from utils.candle_storage import save_candle

symbol_map = {
    "spot": {
        symbol: f"{symbol.lower()}@kline_1m" for symbol in get_all_symbols()["spot"]
    },
    "futures": {
        symbol: f"{symbol.lower()}@kline_1m" for symbol in get_all_symbols()["futures"]
    }
}

price_cache = defaultdict(list)

async def start_ws_listener():
    while True:
        try:
            streams = []
            for market_type in symbol_map:
                streams.extend(symbol_map[market_type].values())

            url = f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"

            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print("[WebSocket] Binance 연결 성공")
                while True:
                    try:
                        message = await ws.recv()
                        data = json.loads(message)

                        if 'data' not in data or 'k' not in data['data']:
                            continue

                        k = data['data']['k']
                        symbol = data['data']['s'].lower()
                        market_type = 'futures' if symbol in symbol_map['futures'] else 'spot'

                        df = pd.DataFrame([{
                            "timestamp": datetime.fromtimestamp(k['t'] / 1000),
                            "open": float(k['o']),
                            "high": float(k['h']),
                            "low": float(k['l']),
                            "close": float(k['c']),
                            "volume": float(k['v'])
                        }])

                        cache_key = f"{market_type}-{symbol}"
                        price_cache[cache_key].append(df.iloc[0])

                        if len(price_cache[cache_key]) > 30:
                            price_cache[cache_key] = price_cache[cache_key][-30:]

                        df_full = pd.DataFrame(price_cache[cache_key])
                        save_candle(symbol, market_type, "M1", df_full, max_rows=3000)

                        update_price(symbol, market_type, float(k['c']))  # ✅ 가격 업데이트 반영

                    except Exception as e:
                        print(f"[WebSocket 내부 오류] {symbol.upper()} | {e}")
                        await asyncio.sleep(1)

        except Exception as outer:
            print(f"[WebSocket 재연결 시도] 오류 발생: {outer}")
            await asyncio.sleep(5)
