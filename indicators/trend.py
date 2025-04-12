# indicators/trend.py

import pandas as pd
from indicators.dow_theory import detect_dow_trend


def detect_trend_string(df: pd.DataFrame) -> str:
    """
    다우이론 기반 추세를 문자열로 변환하는 헬퍼 함수
    예: "상승 전환 (LL → HL)", "하락 지속 (LH → LH)" 등
    """
    try:
        trend = detect_dow_trend(df)
        return trend if trend else ""
    except Exception as e:
        print(f"[추세 분석 오류] {e}")
        return ""
