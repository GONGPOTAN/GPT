# core/workers/send_alert_worker.py

from alert.signal_queue import signal_queue
from alert.telegram_alert import send_telegram_message

async def send_alert_worker():
    print("[📨 알림 워커] 큐 모니터링 시작")
    while True:
        msg = await signal_queue.get()
        try:
            await send_telegram_message(msg)
            print(f"[✅ 알림 전송 완료] {msg}")
        except Exception as e:
            print(f"[❌ 알림 전송 실패] {e}")