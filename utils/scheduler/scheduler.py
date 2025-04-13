# utils/scheduler/scheduler.py

import schedule
import time
import threading

def start_schedulers(candle_worker, daily_report_worker):
    """
    백그라운드 스케줄러 시작
    """
    schedule.every(1).minutes.do(candle_worker)
    schedule.every().day.at("09:00").do(daily_report_worker)

    print("[⏰ 스케줄러] 등록 완료 - 1분마다 분석, 오전 9시 리포트 예정")

    # 최초 1회 즉시 실행
    print("[🚀 즉시 실행] 분석 & 리포트")
    candle_worker()
    daily_report_worker()

    def run_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_loop, daemon=True).start()