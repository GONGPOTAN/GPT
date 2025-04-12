# indicators/volume.py

import pandas as pd

def detect_volume_spike(df: pd.DataFrame, window: int = 20, multiplier: float = 3.0) -> bool:
    """
    거래량 급등 여부 판단 함수
    - window: 평균 거래량을 계산할 기준 캔들 수
    - multiplier: 평균 대비 몇 배 이상일 때 급등으로 간주할지 기준
    """
    if len(df) < window + 1:
        return False

    avg_volume = df['volume'].iloc[-(window+1):-1].mean()
    current_volume = df['volume'].iloc[-1]

    return current_volume > avg_volume * multiplier


def get_volume_comparison(df: pd.DataFrame, window: int = 20) -> tuple:
    """
    텔레그램 메시지용 (평균 거래량, 현재 거래량, 배율) 반환
    → 소수점 2자리까지 반올림하여 반환
    """
    if len(df) < window + 1:
        return (0.00, 0.00, 0.00)

    avg_volume = df['volume'].iloc[-(window+1):-1].mean()
    current_volume = df['volume'].iloc[-1]
    ratio = current_volume / avg_volume if avg_volume > 0 else 0

    return (
        round(avg_volume, 2),
        round(current_volume, 2),
        round(ratio, 2)
    )