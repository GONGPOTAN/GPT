# core/workers/volume_summary_worker.py

import asyncio
from datetime import datetime
from core.state.status_cache import status_cache
from core.queue.signal_queue import signal_queue

VOLUME_LOOKBACK = 20
VOLUME_SPIKE_MULTIPLIER = 10
INTERVAL = 60  # 60초마다 검사

async def volume_summary_worker():
    print("[📈 거래량 유지 워커] 시작됨")

    while True:
        await asyncio.sleep(INTERVAL)
        now = datetime.utcnow()
        minute_key = now.strftime("%Y%m%d%H%M")

        entries = []

        for symbol, tf_data in status_cache.items():
            m1 = tf_data.get("M1", {})
            history = m1.get("volume_history", [])
            current = m1.get("current_volume")
            market = m1.get("market", "")

            if current and len(history) >= VOLUME_LOOKBACK:
                avg_volume = sum(history[-VOLUME_LOOKBACK:]) / VOLUME_LOOKBACK
                if current > avg_volume * VOLUME_SPIKE_MULTIPLIER:
                    entries.append(f"{symbol.upper()} ({market})")

        if entries:
            msg = (
                f"⏳ [거래량 유지] {len(entries)}종목\n"
                f"- {' / '.join(entries)} 에서 거래량이 여전히 높은 상태입니다 (3분 이내)"
            )
            await signal_queue.put({"message": msg})
            print(f"[📤 알림] 거래량 유지 종목: {entries}")