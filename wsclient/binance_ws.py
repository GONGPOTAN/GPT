# wsclient/binance_ws.py

import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from config.symbols import get_all_symbols
from core.signal_queue import signal_queue
from core.volume_summary_worker import volume_ongoing_pool
from core.status_cache import update_price  # ✅ 실시간 가격 업데이트
from alert.alert_cache import mark_alert_sent
from indicators.volume import detect_volume_spike, get_volume_comparison
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
volume_alert_time = defaultdict(lambda: datetime.min)
volume_alert_stage = defaultdict(lambda: "none")
ALERT_INTERVAL_SECONDS = 300

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

                        if detect_volume_spike(df_full):
                            now = datetime.utcnow()
                            last_alert = volume_alert_time[cache_key]
                            state = volume_alert_stage[cache_key]

                            if (now - last_alert).total_seconds() > ALERT_INTERVAL_SECONDS:
                                avg_vol, curr_vol, ratio = get_volume_comparison(df_full)
                                msg = (
                                    f"🔥 [거래량 급등] {symbol.upper()} ({market_type}) - M1\n"
                                    f"- 평균: {avg_vol:,.2f} → 현재: {curr_vol:,.2f} (+{ratio:.2f}배)"
                                )
                                print(f"[M1 거래량 급등] {symbol.upper()} - 평균: {avg_vol:,.2f} / 현재: {curr_vol:,.2f} (x{ratio:.2f})")
                                await signal_queue.put({"message": msg})
                                volume_alert_time[cache_key] = now
                                volume_alert_stage[cache_key] = "active"
                                await mark_alert_sent(f"{symbol}-M1-volume")

                            elif state == "active" and (now - last_alert).total_seconds() <= 180:
                                minute_key = now.strftime("%Y%m%d%H%M")
                                if minute_key not in volume_ongoing_pool:
                                    volume_ongoing_pool[minute_key] = []
                                volume_ongoing_pool[minute_key].append({
                                    "symbol": symbol.upper(),
                                    "market": market_type
                                })
                                volume_alert_stage[cache_key] = "cooldown"

                    except Exception as e:
                        print(f"[WebSocket 내부 오류] {symbol.upper()} | {e}")
                        await asyncio.sleep(1)

        except Exception as outer:
            print(f"[WebSocket 재연결 시도] 오류 발생: {outer}")
            await asyncio.sleep(5)