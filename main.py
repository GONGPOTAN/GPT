import time
import subprocess
from datetime import datetime, timedelta
from app.DataManager.DataManager import update_all_csv
from app.analyzer.analyzer import analyze_all
from app.signal.signal import run_signals

def main():
    caffeinate_proc = subprocess.Popen(["caffeinate", "-imu"])
    print("☕️ caffeinate 활성화됨 – Mac 절전 방지")
    try:
        print("[▶️] DataManager 시작")
        while True:
            start = datetime.now()
            update_all_csv()
            print("[▶️] Analyzer 시작")
            analyze_all()
            print("[✅] Analyzer 구동 완료")
            
            print("[▶️] Signal 분석 시작")
            run_signals()
            print("[✅] Signal 분석 완료")
            
            print("[✅] DataManager 구동 완료")

            next_tick = (start + timedelta(minutes=1)).replace(second=0, microsecond=0)
            sleep_sec = (next_tick - datetime.now()).total_seconds()
            if sleep_sec > 0:
                time.sleep(sleep_sec)

    except Exception as e:
        print(f"[⛔️] 시스템 구동 실패: {e}")
    finally:
        caffeinate_proc.terminate()
        print("☕️ caffeinate 종료됨 – Mac 절전 방지 해제됨")

if __name__ == "__main__":
    main()
