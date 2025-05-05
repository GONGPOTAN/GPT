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
        # print(f"[DEBUG] {symbol}: loaded {len(df)} rows")
        df = df.sort_values("timestamp")
        if len(df) < 2:
            return None
        prev_close = df.iloc[-2]["close"]
        last_close = df.iloc[-1]["close"]
        change = ((last_close - prev_close) / prev_close) * 100

        # Load order book levels if available
        levels_path = f"data/levels/{market_type}/{symbol}.json"
        strong_levels = []
        weak_levels = []
        if os.path.exists(levels_path):
            import json
            with open(levels_path, "r", encoding="utf-8") as f:
                levels_data = json.load(f)
                strong_levels = [float(p) for p in levels_data.get("strong", []) if p is not None]
                weak_levels = [float(p) for p in levels_data.get("weak", []) if p is not None]

        strong_str = " | ".join(f"{p:,.2f}" for p in strong_levels) if strong_levels else "없음"
        weak_str = " | ".join(f"{p:,.2f}" for p in weak_levels) if weak_levels else "없음"

        sign = "+" if change >= 0 else "-"
        change_str = f"{sign}{abs(change):.2f}%"

        message = (
            f"🔹 {symbol}\n"
            f"- 종가: {last_close:,.2f} USDT ({change_str})\n"
            f"- 🧱 강 매물대: {strong_str}\n"
            f"- 🍃 약 매물대: {weak_str}"
        )
        return message
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")
        return f"🔹 {symbol}\n- 데이터 없음"

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
                section.append(result)
        if len(section) > 1:
            messages.extend(section)

    text = "\n\n".join(messages)
    send_telegram_message(text)
