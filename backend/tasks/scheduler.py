import schedule
import time
import threading

def register(loop):
    """
    schedule 기반 경량 스케줄러.
    주기적으로 특정 함수들을 실행하기 위한 등록기입니다.
    """

    from core.workers.rsi_trend_worker import rsi_trend_worker
    from core.workers.volume_summary_worker import volume_summary_worker
    from core.workers.daily_report_worker import daily_report_worker  # ✅ 추가

    def run_rsi_worker():
        loop.create_task(rsi_trend_worker())

    def run_volume_summary():
        loop.create_task(volume_summary_worker())

    def run_daily_report():
        loop.create_task(daily_report_worker())  # ✅ 매일 아침 9시 실행할 리포트

    # 🕒 주기 등록
    schedule.every(1).minutes.do(run_rsi_worker)
    schedule.every(1).minutes.do(run_volume_summary)
    schedule.every().day.at("00:00").do(run_daily_report)  # ✅ JST 09:00 기준 (UTC 00:00)

    print("[⏰ 스케줄러 등록 완료] RSI + 거래량 + 데일리 리포트 스케줄링됨")

    # 🚀 즉시 1회 실행
    run_rsi_worker()
    run_volume_summary()
    run_daily_report()  # 🔧 즉시 리포트 실행

    def run_loop():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run_loop, daemon=True).start()
