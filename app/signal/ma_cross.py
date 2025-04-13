import pandas as pd

def check_signal(df: pd.DataFrame, interval: str) -> list:
    results = []
    if not {"ma7", "ma30", "ma99"}.issubset(df.columns) or len(df) < 2:
        return results

    latest = df.iloc[-1]
    previous = df.iloc[-2]

    # 단기 MA7 vs MA30
    # print("[단기] prev MA7:", previous["ma7"], "MA30:", previous["ma30"])
    # print("[단기] curr MA7:", latest["ma7"], "MA30:", latest["ma30"])
    if previous["ma7"] < previous["ma30"] and latest["ma7"] > latest["ma30"]:
        results.append({
            "type": "ma_cross",
            "scope": "단기",
            "detail": f"골든크로스 발생 (MA7: {latest['ma7']:.2f}, MA30: {latest['ma30']:.2f})"
        })
    elif previous["ma7"] > previous["ma30"] and latest["ma7"] < latest["ma30"]:
        results.append({
            "type": "ma_cross",
            "scope": "단기",
            "detail": f"데드크로스 발생 (MA7: {latest['ma7']:.2f}, MA30: {latest['ma30']:.2f})"
        })

    # 중장기 MA30 vs MA99
    # print("[중장기] prev MA30:", previous["ma30"], "MA99:", previous["ma99"])
    # print("[중장기] curr MA30:", latest["ma30"], "MA99:", latest["ma99"])
    if previous["ma30"] < previous["ma99"] and latest["ma30"] > latest["ma99"]:
        results.append({
            "type": "ma_cross",
            "scope": "중장기",
            "detail": f"골든크로스 발생 (MA30: {latest['ma30']:.2f}, MA99: {latest['ma99']:.2f})"
        })
    elif previous["ma30"] > previous["ma99"] and latest["ma30"] < latest["ma99"]:
        results.append({
            "type": "ma_cross",
            "scope": "중장기",
            "detail": f"데드크로스 발생 (MA30: {latest['ma30']:.2f}, MA99: {latest['ma99']:.2f})"
        })

    return results
