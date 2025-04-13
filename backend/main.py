# backend/main.py

import asyncio
import platform
import subprocess
import uvicorn
import nest_asyncio

from backend_api.api import app
from backend.tasks.start_ws import start_ws
from backend.tasks.start_price_worker import start_price_worker
from backend.tasks.start_rsi_worker import start_rsi_worker
from backend.tasks.start_signal_worker import start_signal_worker
from backend.tasks.start_volume_worker import start_volume_worker
from backend.tasks.scheduler import register as register_scheduler

def keep_mac_awake():
    if platform.system() == "Darwin":
        subprocess.Popen(["caffeinate", "-i"])
        print("[🍎 Mac 잠자기 방지] caffeinate 실행 중")

def start_fastapi():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    loop = asyncio.get_event_loop()
    loop.create_task(server.serve())

if __name__ == "__main__":
    print("🚀 GPT Trading Bot 시스템 시작")

    keep_mac_awake()
    nest_asyncio.apply()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_fastapi()

    # 🎯 태스크 등록
    loop.create_task(start_ws())
    loop.create_task(start_price_worker())
    loop.create_task(start_rsi_worker())
    loop.create_task(start_signal_worker())
    loop.create_task(start_volume_worker())

    # 🕒 스케줄러 등록
    register_scheduler(loop)

    loop.run_forever()