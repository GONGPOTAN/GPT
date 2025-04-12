# alert/signal_checker.py

import asyncio
import datetime
from config.symbols import get_all_symbols
from indicators.rsi import calculate_rsi_sma
from indicators.ma import calculate_sma, detect_ma_crossover
from indicators.dow_theory import detect_dow_trend
from indicators.volume import detect_volume_spike
from modules.binance_api import get_klines, get_24hr_change
from alert.telegram_alert import send_telegram_message
from alert.alert_cache import is_alert_sent, mark_alert_sent, init_db
from utils.candle_storage import save_candle

MAX_ROWS = {
    "M15": 1500,
    "H1": 1500,
    "H4": 1000,
    "D": 730
}

# 시그널 분석 주기 실행 함수 (M15 이상 전용)
async def check_higher_timeframe_signals():
    await init_db()
    intervals = {
        "M15": "15m",
        "H1": "1h",
        "H4": "4h",
        "D": "1d"
    }
    for market_type, symbols in get_all_symbols().items():
        for symbol in symbols:
            for key, interval in intervals.items():
                df = get_klines(symbol, market_type, interval=interval, limit=100)
                if df.empty: continue

                save_candle(symbol, market_type, key, df, max_rows=MAX_ROWS[key])

                df["rsi"] = calculate_rsi_sma(df["close"])
                latest_rsi = df["rsi"].iloc[-1]

                if latest_rsi >= 70:
                    alert_id = f"{symbol}-{key}-rsi-overbought"
                    if not await is_alert_sent(alert_id):
                        msg = f"🔴 [RSI 과매수] {symbol.upper()} ({market_type}) - {key}\n- RSI: {latest_rsi:.2f}"
                        await mark_alert_sent(alert_id)
                        await send_telegram_message(msg)

                elif latest_rsi <= 30:
                    alert_id = f"{symbol}-{key}-rsi-oversold"
                    if not await is_alert_sent(alert_id):
                        msg = f"🔵 [RSI 과매도] {symbol.upper()} ({market_type}) - {key}\n- RSI: {latest_rsi:.2f}"
                        await mark_alert_sent(alert_id)
                        await send_telegram_message(msg)

                if key == "M15":
                    df["sma"] = calculate_sma(df)
                    direction = detect_ma_crossover(df)
                    if direction:
                        alert_id = f"{symbol}-{key}-ma30-{direction}"
                        if not await is_alert_sent(alert_id):
                            price = df["close"].iloc[-1]
                            ma = df["sma"].iloc[-1]
                            direction_txt = "상향 돌파" if direction == "bullish" else "하향 돌파"
                            emoji = "📈💥" if direction == "bullish" else "📉⚠️"
                            msg = f"{emoji} [MA30 {direction_txt}] {symbol.upper()} ({market_type}) - {key}\n- 현재가: {price:,.1f} USDT\n- MA30: {ma:,.1f} USDT"
                            await mark_alert_sent(alert_id)
                            await send_telegram_message(msg)

                trend_msg = detect_dow_trend(df)
                if trend_msg:
                    import re
                    trend_type_match = re.search(r"\\((.*?)\\)", trend_msg)
                    trend_type = trend_type_match.group(1).replace(" → ", "-") if trend_type_match else "unknown"
                    alert_id = f"{symbol}-{key}-dow-{trend_type.lower()}"

                    if not await is_alert_sent(alert_id):
                        emoji = "⚠️📉" if "하락" in trend_msg else "⚠️📈"
                        msg = f"{emoji} [추세 감지] {symbol.upper()} ({market_type}) - {key}\n- {trend_msg}"
                        await mark_alert_sent(alert_id)
                        await send_telegram_message(msg)

# 매일 오전 9시 (UTC 00시) 전일 변동률 리포트
async def send_daily_report():
    await init_db()
    today = datetime.datetime.utcnow()
    weekday_kor = ["월", "화", "수", "목", "금", "토", "일"]
    wday = weekday_kor[today.weekday()]
    title = today.strftime(f"📊 [전일 변동률 리포트] %Y-%m-%d ({wday})")

    report = ""
    for market_type, symbols in get_all_symbols().items():
        for symbol in symbols:
            pct = get_24hr_change(symbol, market_type)
            report += f"- {symbol.upper()}: {pct:+.2f}%\n"

    await send_telegram_message(f"{title}\n{report}")