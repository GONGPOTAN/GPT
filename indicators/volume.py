# indicators/volume.py

import pandas as pd

def detect_volume_spike(df: pd.DataFrame, window: int = 20, threshold: float = 3.0) -> bool:
    """
    거래량 급등 여부를 판단합니다.
    최근 window 개의 평균 거래량 대비 마지막 거래량이 threshold 배 이상이면 급등으로 간주합니다.
    """
    if len(df) < window + 1:
        return False

    recent_volumes = df["volume"].iloc[-(window+1):-1]
    average_volume = recent_volumes.mean()
    current_volume = df["volume"].iloc[-1]

    return current_volume > average_volume * threshold