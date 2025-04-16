def format_message(signal_type, market_type, symbol, interval, detail):
    if signal_type == "ma_cross":
        direction = "골든크로스" if "골든" in detail else "데드크로스"
        emoji = "📈" if "골든" in detail else "📉"
        return f"""{emoji} MA 크로스 시그널
📍 {market_type}/{symbol} {interval}
{direction} 발생 ({detail.split('(',1)[-1]}"""

    elif signal_type == "breakout":
        direction = "상향 돌파" if "상향" in detail else "하향 돌파"
        return f"""📊 브레이크아웃 시그널
📍 {market_type}/{symbol} {interval}
{direction} ({detail.split('(',1)[-1]}"""

    elif signal_type == "rsi_signal":
        direction = "과매도" if "과매도" in detail else "과매수"
        emoji = "📉" if "과매도" in detail else "📈"
        return f"""{emoji} RSI 시그널
📍 {market_type}/{symbol} {interval}
{direction} 진입 ({detail})"""

    elif signal_type == "volume_spike":
        return f"""📊 거래량 급등 시그널
📍 {market_type}/{symbol} {interval}
{detail}"""

    else:
        return f"""📌 시그널 감지
📍 {market_type}/{symbol} {interval}
{detail}"""
