# alert/signal_checker.py

import asyncio
from config.symbols import get_all_symbols
from indicators.rsi import calculate_rsi_sma
from indicators.ma import calculate_sma, detect_ma_crossover
from core.services.binance_api import get_klines
from alert.telegram_alert import send_telegram_message
from alert.alert_cache import is_alert_sent, mark_alert_sent, init_db
from utils.io.candle_storage import save_candle

MAX_ROWS = {
    "M15": 1500,
    "H1": 1500,
    "H4": 1000,
    "D": 730
}

async def check_signals(symbol: str, market_type: str):
    await init_db()
    intervals = {"M15": "15m", "H1": "1h", "H4": "4h", "D": "1d"}

    for key, interval in intervals.items():
        df = get_klines(symbol, market_type, interval=interval, limit=100)
        if df.empty:
            continue

        save_candle(symbol, market_type, key, df, max_rows=MAX_ROWS[key])

        # RSI 분석
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

        # MA30 돌파 분석 (M15만)
        if key == "M15":
            df["sma"] = calculate_sma(df)
            direction = detect_ma_crossover(df)

            if direction:
                alert_id = f"{symbol}-{key}-ma30-{direction}"
                if not await is_alert_sent(alert_id):
                    price = df["close"].iloc[-1]
                    ma = df["sma"].iloc[-1]
                    direction_txt = "상향 돌파" if direction == "bullish" else "하향 돌파"
                    emoji = "📈" if direction == "bullish" else "⚠️"
                    msg = (
                        f"{emoji} [MA30 {direction_txt}] {symbol.upper()} ({market_type}) - {key}\n"
                        f"- 현재가: {price:,.1f} USDT\n- MA30: {ma:,.1f} USDT"
                    )
                    await mark_alert_sent(alert_id)
                    await send_telegram_message(msg)