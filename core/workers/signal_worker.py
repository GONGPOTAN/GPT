# core/workers/signal_worker.py

import asyncio
from alert.telegram_alert import send_telegram_message
from core.queue.signal_queue import signal_queue

SEND_DELAY = 0.5
ERROR_RETRY_DELAY = 1.0

async def signal_worker():
    print("[📨 시그널 워커] 시작됨 - 텔레그램 메시지 큐 처리 중...")

    while True:
        try:
            signal = await signal_queue.get()
            message = signal.get("message")

            if message:
                await send_telegram_message(message)
                print(f"[📤 전송 완료] {message[:50]}...")
                await asyncio.sleep(SEND_DELAY)

        except Exception as e:
            print(f"[❌ 텔레그램 전송 오류] {e}")
            await asyncio.sleep(ERROR_RETRY_DELAY)