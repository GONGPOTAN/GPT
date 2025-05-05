import pandas as pd

def extract_levels(symbol, market_type):
    """
    Extract strong and weak levels from price data for a given symbol and market type.
    Returns a dict: {"strong": [...], "weak": [...]}
    """
    path = f"data/price/{market_type}/D1/{symbol}.csv"
    try:
        df = pd.read_csv(path, parse_dates=["timestamp"])
        closes = df["close"]

        # Example: use quantiles as strong/weak levels
        strong = [
            round(closes.quantile(0.9), 2),
            round(closes.quantile(0.7), 2),
            round(closes.quantile(0.5), 2),
        ]
        weak = [
            round(closes.quantile(0.3), 2),
            round(closes.quantile(0.1), 2),
        ]

        return {"strong": strong, "weak": weak}
    except Exception as e:
        print(f"[⚠️] {symbol} 데이터 로딩 실패: {e}")
        return {"strong": [], "weak": []}