import pandas as pd

def check_signal(df: pd.DataFrame, interval: str) -> list:
    results = []

    if interval != "M15":
        return results
    if not {"close", "ma30"}.issubset(df.columns) or len(df) < 2:
        return results

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    # 상향 돌파
    if prev["close"] < prev["ma30"] and curr["close"] > curr["ma30"]:
        results.append({
            "type": "breakout",
            "target": "MA30",
            "scope": "M15",
            "detail": f"상향돌파 (Close: {curr['close']:.2f} > MA30: {curr['ma30']:.2f})"
        })
    # 하향 돌파
    elif prev["close"] > prev["ma30"] and curr["close"] < curr["ma30"]:
        results.append({
            "type": "breakout",
            "target": "MA30",
            "scope": "M15",
            "detail": f"하향돌파 (Close: {curr['close']:.2f} < MA30: {curr['ma30']:.2f})"
        })

    return results
