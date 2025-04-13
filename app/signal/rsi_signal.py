import pandas as pd

def check_signal(df: pd.DataFrame, interval: str) -> list:
    results = []

    allowed_intervals = ["H1", "H4", "D1", "W1"]
    if interval not in allowed_intervals:
        return results
    if "close" not in df.columns or len(df) < 15:
        return results

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    recent_rsi = rsi.iloc[-1]
    if pd.isna(recent_rsi):
        return results

    if recent_rsi > 70:
        results.append({
            "type": "rsi_signal",
            "scope": interval,
            "detail": f"RSI 과매수 (현재 RSI: {recent_rsi:.2f})"
        })
    elif recent_rsi < 30:
        results.append({
            "type": "rsi_signal",
            "scope": interval,
            "detail": f"RSI 과매도 (현재 RSI: {recent_rsi:.2f})"
        })

    return results
