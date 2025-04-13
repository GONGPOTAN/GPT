# backend/tasks/start_ws.py
import asyncio
from wsclient.binance_ws import start_ws_listener

async def start_ws():
    print("[🌐 WebSocket] 실시간 데이터 수신 시작")
    asyncio.create_task(start_ws_listener())