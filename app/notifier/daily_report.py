import os
import pandas as pd
from datetime import datetime, timedelta
from app.notifier.telegram_notifier import send_telegram_message
from config.symbols import SYMBOLS

JST = timedelta(hours=9)

def get_yesterday_change(symbol: str, market_type: str) -> str:
    path = f"data/price/{market_type}/D1/{symbol}.csv"
    try:
        df = pd.read_csv(path, parse_dates=["timestamp"])
        df = df.sort_values("timestamp")
        if len(df) < 2:
            return None
        prev_close = df.iloc[-2]["close"]
        last_close = df.iloc[-1]["close"]
        change = ((last_close - prev_close) / prev_close) * 100
        return f"{symbol}: {change:.2f}%"
    except Exception as e:
        return f"{symbol}: 데이터 없음"

def report_daily_change():
    now_jst = datetime.utcnow() + JST
    header = f"📈 전일 대비 변동률 리포트 ({now_jst.strftime('%Y-%m-%d')})"
    messages = [header]

    for market_type, symbols in SYMBOLS.items():
        if not symbols:
            continue
        section = [f"\n📊 {market_type.upper()}"]
        for symbol in symbols:
            result = get_yesterday_change(symbol, market_type)
            if result:
                section.append(f"- {result}")
        if len(section) > 1:
            messages.extend(section)

    text = "\n".join(messages)
    send_telegram_message(text)
