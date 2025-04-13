# wsclient/binance_ws.py
import asyncio
import websockets
import json
from wsclient.utils.stream_builder import build_stream_url
from wsclient.handlers.candle_handler import handle_candle

async def start_ws_listener():
    while True:
        try:
            url = build_stream_url()
            async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:
                print(f"[WebSocket] Binance 연결됨: {url}")
                while True:
                    try:
                        message = await ws.recv()
                        await handle_candle(message)
                    except Exception as e:
                        print(f"[WebSocket 내부 오류] {e}")
                        await asyncio.sleep(1)
        except Exception as outer:
            print(f"[WebSocket 재연결 시도 중] 오류: {outer}")
            await asyncio.sleep(5)