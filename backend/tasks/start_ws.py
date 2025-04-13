# backend/tasks/start_ws.py

from wsclient.binance_ws import start_ws_listener

async def start_ws():
    print("[🧩 WS 태스크] WebSocket 리스너 시작")
    await start_ws_listener()