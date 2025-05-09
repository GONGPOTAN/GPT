import pandas as pd
from app.analyzer.ma import analyze_ma
from app.analyzer.rsi import analyze_rsi
from app.analyzer.dow import analyze_dow
from app.analyzer.level_extractor import extract_levels
from app.logger.logger import log_analysis_result
from config.symbols import SYMBOLS
from config.analysis import ANALYSIS_CONFIG

def analyze_all():
    intervals = ["M1", "M15", "H1", "H4", "D1", "W1"]
    results = []

    for market_type, symbols in SYMBOLS.items():
        for symbol in symbols:
            for interval in intervals:
                path = f"data/price/{market_type}/{interval}/{symbol}.csv"
                try:
                    df = pd.read_csv(path, parse_dates=["timestamp"])
                    ma_result = analyze_ma(df)
                    rsi_result = analyze_rsi(df)
                    dow_result = analyze_dow(df)
                    level_result = extract_levels(symbol, market_type)
                    combined_result = {**ma_result, **rsi_result, **dow_result, **level_result}

                    log_analysis_result(market_type, symbol, interval, combined_result)
                    results.append({
                        "market_type": market_type,
                        "symbol": symbol,
                        "interval": interval,
                        "result": combined_result
                    })
                except FileNotFoundError:
                    continue

    return results

if __name__ == "__main__":
    analyze_all()
