# main.py

import asyncio
import subprocess
import platform
import threading
from dotenv import load_dotenv
load_dotenv()

# Mac 환경에서 시스템 잠자기만 방지 (모니터는 꺼질 수 있음)
if platform.system() == "Darwin":
    subprocess.Popen(["caffeinate", "-i"])

# 주요 모듈 불러오기
from wsclient.binance_ws import start_ws_listener
from alert.signal_checker import check_higher_timeframe_signals, send_daily_report
from utils.scheduler import start_schedulers
from core.signal_worker import signal_worker
from core.volume_summary_worker import volume_summary_worker  # 거래량 유지 요약 워커
from core.rsi_trend_worker import rsi_trend_worker  # ✅ RSI/Trend 캐시 업데이트 워커

# ✅ FastAPI 서버 함께 실행
import uvicorn
from backend_api import api  # ← FastAPI 앱(app)은 여기서 가져옵니다.

def start_fastapi():
    # ✅ Render 등 외부 서비스에서 접근 가능하도록 0.0.0.0 으로 변경
    uvicorn.run(api.app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    print("🚀 GPT-Trading-Bot 시스템 시작")
    print(" - 실시간 WebSocket 구독 (M1)")
    print(" - 시그널 분석 (M15~D)")
    print(" - 텔레그램 알림 송신")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # ✅ FastAPI 백그라운드 실행
    threading.Thread(target=start_fastapi, daemon=True).start()

    # 주요 비동기 작업 등록
    loop.create_task(start_ws_listener())
    loop.create_task(signal_worker())
    loop.create_task(volume_summary_worker())
    loop.create_task(rsi_trend_worker())  # ✅ RSI 및 추세 캐시 갱신

    # 시그널 분석/리포트 예약
    start_schedulers(
        m15_handler=lambda: asyncio.run(check_higher_timeframe_signals()),
        daily_handler=lambda: asyncio.run(send_daily_report())
    )

    loop.run_forever()