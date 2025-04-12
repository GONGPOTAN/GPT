# core/volume_summary_worker.py

import asyncio
from datetime import datetime
from core.signal_queue import signal_queue

# 유지 종목을 시간 단위로 그룹핑
volume_ongoing_pool = {}

async def volume_summary_worker():
    while True:
        await asyncio.sleep(60)  # 1분마다 체크
        now = datetime.utcnow()
        minute_key = now.strftime("%Y%m%d%H%M")
        if minute_key in volume_ongoing_pool:
            entries = volume_ongoing_pool.pop(minute_key)
            if entries:
                symbol_list = ", ".join([f"{e['symbol']} ({e['market']})" for e in entries])
                msg = (
                    f"⏳ [거래량 유지] {len(entries)}종목\n"
                    f"- {symbol_list} 에서 거래량이 여전히 높은 상태입니다 (3분 이내)"
                )
                await signal_queue.put({"message": msg})
