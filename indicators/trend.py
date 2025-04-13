# indicators/trend.py

def detect_trend_string(df):
    from indicators.dow_theory import detect_dow_trend

    trend = detect_dow_trend(df)
    if trend == "HH-HL":
        return "📈 상승 추세"
    elif trend == "LL-LH":
        return "📉 하락 추세"
    elif trend == "확장형":
        return "🔁 변동성 확장"
    elif trend == "중립":
        return "⏸ 중립 구간"
    else:
        return None