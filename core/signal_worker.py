# core/signal_worker.py

import asyncio
from alert.telegram_alert import send_telegram_message
from core.signal_queue import signal_queue

# 큐에서 메시지를 순차적으로 꺼내 전송하는 워커
async def signal_worker():
    print("[시그널 워커] 시작됨 - 큐 대기 중...")
    while True:
        try:
            signal = await signal_queue.get()
            message = signal.get("message")
            if message:
                await send_telegram_message(message)
            await asyncio.sleep(0.5)  # 텔레그램 rate limit 보호
        except Exception as e:
            print(f"[시그널 워커] 오류 발생: {e}")
            await asyncio.sleep(1)
