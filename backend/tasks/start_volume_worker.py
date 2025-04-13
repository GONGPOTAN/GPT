# backend/tasks/start_volume_worker.py

from core.workers.volume_summary_worker import volume_summary_worker

async def start_volume_worker():
    print("[📈 거래량 태스크] 거래량 유지 감지 워커 실행")
    await volume_summary_worker()