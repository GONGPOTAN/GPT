# indicators/dow_theory.py

import pandas as pd

def format_price(val: float) -> str:
    return f"{val:,.6f}".rstrip("0").rstrip(".")

def detect_dow_trend(df: pd.DataFrame) -> str:
    """
    최근 4개 캔들의 고점/저점 비교를 통해 다우이론 기반 추세 판단
    - 상승 추세 지속: HL → HH, 이전보다 높아야 함
    - 하락 추세 지속: LL → LH, 이전보다 낮아야 함
    - 전환은 고점/저점의 구조가 바뀔 때
    """
    if len(df) < 4:
        return None

    highs = df['high'].iloc[-4:].values
    lows = df['low'].iloc[-4:].values

    prev2_low, prev_low, curr_low = lows[-3], lows[-2], lows[-1]
    prev2_high, prev_high, curr_high = highs[-3], highs[-2], highs[-1]

    # 상승 추세 지속: HL → HH, 이전보다 높아야 함
    if prev_low > prev2_low and curr_high > prev_high:
        return f"상승 추세 지속 (HL → HH) [{format_price(prev_low)} → {format_price(curr_high)}]"

    # 하락 추세 지속: LL → LH, 이전보다 낮아야 함
    if prev_low < prev2_low and curr_high < prev_high:
        return f"하락 추세 지속 (LL → LH) [{format_price(prev_low)} → {format_price(curr_high)}]"

    # 상승 전환: LL → HL
    if prev2_low > prev_low < curr_low:
        return f"상승 전환 (LL → HL) [{format_price(prev_low)} → {format_price(curr_low)}]"

    # 하락 전환: HH → LH
    if prev2_high < prev_high > curr_high:
        return f"하락 전환 (HH → LH) [{format_price(prev_high)} → {format_price(curr_high)}]"

    return None
