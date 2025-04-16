import time
import subprocess
import schedule
from datetime import datetime, timedelta
from app.datamanager.datamanager import update_all_csv
from app.analyzer.analyzer import analyze_all
from app.signal.signal import run_signals
from app.logger.logger import safe_log
from app.notifier.daily_report import report_daily_change

def main():
    schedule.every().day.at("09:00").do(report_daily_change)

    # Mac 절전 방지
    caffeinate_proc = subprocess.Popen(["caffeinate"])
    safe_log("☕️ caffeinate 활성화됨 – Mac 절전 방지")

    try:
        while True:
            schedule.run_pending()
            start = datetime.now()
            update_all_csv()
            safe_log("[▶️] Analyzer 시작")
            analyze_all()
            safe_log("[✅] Analyzer 구동 완료")
            
            safe_log("[▶️] Signal 분석 시작")
            run_signals()
            safe_log("[✅] Signal 분석 완료")

            safe_log("[✅] datamanager 구동 완료")

            next_tick = (start + timedelta(minutes=1)).replace(second=0, microsecond=0)
            sleep_sec = (next_tick - datetime.now()).total_seconds()
            if sleep_sec > 0:
                time.sleep(sleep_sec)

    except Exception as e:
        safe_log(f"[⛔️] 시스템 구동 실패: {e}")
    finally:
        caffeinate_proc.terminate()
        safe_log("☕️ caffeinate 종료됨 – Mac 절전 방지 해제됨")

if __name__ == "__main__":
    main()
