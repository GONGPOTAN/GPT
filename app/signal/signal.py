import pandas as pd
import importlib
from config.symbols import SYMBOLS

SIGNAL_MODULES = [
    "ma_cross",
    "breakout",
    "volume_spike",
    "rsi_signal",
]

def run_signals():
    intervals = ["M1", "M15", "H1", "H4", "D1", "W1"]

    for market_type, symbols in SYMBOLS.items():
        for symbol in symbols:
            for interval in intervals:
                path = f"data/price/{market_type}/{interval}/{symbol}.csv"
                try:
                    df = pd.read_csv(path, parse_dates=["timestamp"])

                    for mod in SIGNAL_MODULES:
                        signal_module = importlib.import_module(f"app.signal.{mod}")
                        signals = signal_module.check_signal(df, interval)
                        if signals:
                            print(f"[시그널 발생] {market_type}/{symbol} {interval}")
                            # for sig in signals:
                            #     print(sig)

                except FileNotFoundError:
                    continue

if __name__ == "__main__":
    run_signals()
