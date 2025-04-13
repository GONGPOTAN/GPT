# backend/tasks/start_price_worker.py

from core.workers.price_worker import price_worker

async def start_price_worker():
    print("[📊 가격 태스크] 가격 워커 실행")
    await price_worker()