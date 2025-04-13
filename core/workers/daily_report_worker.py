# core/workers/daily_report_worker.py

import asyncio
from datetime import datetime, timedelta
from config.symbols import get_all_symbols
from core.services.binance_api import get_klines
from alert.telegram_alert import send_telegram_message

def get_kst_date():
    return datetime.utcnow() + timedelta(hours=9)

async def daily_report_worker():
    print("[📊 데일리 리포트] 시작됨")

    now_kst = get_kst_date()
    today = now_kst.date()
    yesterday = today - timedelta(days=1)
    weekday = ["(월)", "(화)", "(수)", "(목)", "(금)", "(토)", "(일)"][yesterday.weekday()]

    header = f"📆 [{yesterday} {weekday}] 전일 종가 기준 변동률"
    messages = [header]

    for market_type, symbols in get_all_symbols().items():
        for symbol in symbols:
            df = get_klines(symbol, market_type, interval="1d", limit=2)
            if len(df) < 2:
                continue

            prev_close = df["close"].iloc[-2]
            latest_close = df["close"].iloc[-1]
            change_pct = ((latest_close - prev_close) / prev_close) * 100
            emoji = "🔼" if change_pct > 0 else "🔽"

            line = f"{emoji} {symbol.upper()} ({market_type}) : {change_pct:+.2f}%"
            messages.append(line)

    final_message = "\n".join(messages)
    await send_telegram_message(final_message)
    print("[✅ 데일리 리포트] 텔레그램 전송 완료")