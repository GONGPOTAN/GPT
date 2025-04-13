import pandas as pd

def check_signal(df: pd.DataFrame, interval: str) -> list:
    results = []

    if interval != "M1":
        return results
    if not "volume" in df.columns or len(df) < 21:
        return results

    recent_volume = df.iloc[-1]["volume"]
    avg_volume = df["volume"].iloc[-21:-1].mean()

    if recent_volume > avg_volume * 10:
        results.append({
            "type": "거래량급등",
            "scope": "M1",
            "detail": f"1분 거래량이 평균({avg_volume:.2f})의 10배 초과 (현재: {recent_volume:.2f})"
        })

    return results
