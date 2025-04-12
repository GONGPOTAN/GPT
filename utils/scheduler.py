# utils/scheduler.py

import schedule
import time
import threading

def start_schedulers(m15_handler, daily_handler):
    # 매 1분마다 M15~D 캔들 분석 실행
    schedule.every(1).minutes.do(m15_handler)

    # 시스템 시간 기준 오전 9시에 전일 리포트 실행 (UTC 시스템 환경 대응)
    schedule.every().day.at("09:00").do(daily_handler)

    print("[스케줄러] 초기 실행 시작")
    m15_handler()
    daily_handler()

    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run, daemon=True).start()
