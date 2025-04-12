# core/volume_summary_worker.py

import asyncio
from datetime import datetime
from core.signal_queue import signal_queue
from core.status_cache import status_cache  # ✅ 실시간 거래량 정보 불러오기

# 유지 종목을 시간 단위로 그룹핑
volume_ongoing_pool = {}

# 거래량 급등 판단 기준
VOLUME_LOOKBACK = 20  # 최근 20개 평균
VOLUME_SPIKE_MULTIPLIER = 10  # ✅ 평균의 10배 초과 시 급등 판단

async def volume_summary_worker():
    while True:
        await asyncio.sleep(60)  # 1분마다 체크
        now = datetime.utcnow()
        minute_key = now.strftime("%Y%m%d%H%M")

        # ✅ 실시간 캐시 기반으로 거래량 급등 종목 선별
        entries = []
        for symbol, tf_data in status_cache.items():
            m1_data = tf_data.get("M1")
            if not m1_data:
                continue

            volume_history = m1_data.get("volume_history", [])
            current_volume = m1_data.get("current_volume")
            market = m1_data.get("market", "")

            if (
                current_volume is not None
                and len(volume_history) >= VOLUME_LOOKBACK
            ):
                avg_volume = sum(volume_history[-VOLUME_LOOKBACK:]) / VOLUME_LOOKBACK
                if current_volume > avg_volume * VOLUME_SPIKE_MULTIPLIER:
                    entries.append({"symbol": symbol, "market": market})

        if entries:
            volume_ongoing_pool[minute_key] = entries
            symbol_list = ", ".join([f"{e['symbol']} ({e['market']})" for e in entries])
            msg = (
                f"⏳ [거래량 유지] {len(entries)}종목\n"
                f"- {symbol_list} 에서 거래량이 여전히 높은 상태입니다 (3분 이내)"
            )
            await signal_queue.put({"message": msg})