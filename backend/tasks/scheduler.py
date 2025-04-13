# backend/tasks/scheduler.py

import schedule
import time
import threading

def register(loop):
    """
    APScheduler처럼 동작하는 경량 schedule 등록기.
    주기적으로 특정 함수들을 실행하기 위한 스케줄러입니다.
    """

    from core.workers.rsi_trend_worker import rsi_trend_worker
    from core.workers.volume_summary_worker import volume_summary_worker

    def run_rsi_worker():
        loop.create_task(rsi_trend_worker())

    def run_volume_summary():
        loop.create_task(volume_summary_worker())

    # 1분 간격으로 중기 분석
    schedule.every(1).minutes.do(run_rsi_worker)
    schedule.every(1).minutes.do(run_volume_summary)

    print("[⏰ 스케줄러 등록 완료] RSI + 거래량 스케줄링됨")

    # 즉시 1회 실행
    run_rsi_worker()
    run_volume_summary()

    def run_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_loop, daemon=True).start()