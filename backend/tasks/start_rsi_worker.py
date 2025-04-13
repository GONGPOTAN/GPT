# backend/tasks/start_rsi_worker.py

from core.workers.rsi_trend_worker import rsi_trend_worker

async def start_rsi_worker():
    print("[📈 RSI 태스크] RSI/Trend 워커 실행")
    await rsi_trend_worker()