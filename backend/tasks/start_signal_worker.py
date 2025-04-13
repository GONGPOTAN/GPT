# backend/tasks/start_signal_worker.py

from core.workers.signal_worker import signal_worker

async def start_signal_worker():
    print("[📨 시그널 태스크] 텔레그램 전송 워커 실행")
    await signal_worker()