import os
import time
from app.datamanager import datamanager
from app.datamanager.price_fetcher import should_update
from config.symbols import SYMBOLS
from datetime import datetime, timedelta
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

INTERVALS = ["1m", "15m", "1h", "4h", "1d", "1w"]

def save_candles_to_csv():
    dm = datamanager()
    interval_map = {
        "1m": "M1",
        "15m": "M15",
        "1h": "H1",
        "4h": "H4",
        "1d": "D1",
        "1w": "W1"
    }

    def process_symbol(market_type, symbol, interval):
        try:
            df = dm.get_candles(symbol, interval, market=market_type)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("Asia/Tokyo").dt.tz_localize(None)
            save_interval = interval_map[interval]
            dir_path = os.path.join("data/price", market_type, save_interval)
            os.makedirs(dir_path, exist_ok=True)
            file_path = os.path.join(dir_path, f"{symbol}.csv")
            df.to_csv(file_path, index=False)
            if __name__ == "__main__":
                print(f"[✓] {symbol} {interval} ({market_type}) 저장 완료")
        except Exception as e:
            if __name__ == "__main__":
                print(f"[✗] {symbol} {interval} ({market_type}) 저장 실패: {e}")

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = []
        for market_type, symbols in SYMBOLS.items():
            for symbol in symbols:
                for interval in INTERVALS:
                    futures.append(executor.submit(process_symbol, market_type, symbol, interval))

        for future in as_completed(futures):
            future.result()

update_all_csv = save_candles_to_csv

if __name__ == "__main__":
    while True:
        start = datetime.now()
        save_candles_to_csv()

        next_tick = (start + timedelta(minutes=1)).replace(second=0, microsecond=0)
        sleep_sec = (next_tick - datetime.now()).total_seconds()

        if sleep_sec > 0:
            time.sleep(sleep_sec)