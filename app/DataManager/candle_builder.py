import pandas as pd
from app.analyzer.ma import analyze_ma

class CandleBuilder:
    def build(self, raw_data: list) -> pd.DataFrame:
        df = pd.DataFrame(raw_data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])

        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

        ma_result = analyze_ma(df)
        for key, value in ma_result.items():
            df[key] = value

        return df

    def merge_with_existing(self, new_df: pd.DataFrame, csv_path: str) -> pd.DataFrame:
        try:
            existing_df = pd.read_csv(csv_path, parse_dates=["timestamp"])
            df = pd.concat([existing_df, new_df])
            df = df.drop_duplicates(subset="timestamp").sort_values("timestamp")
        except FileNotFoundError:
            df = new_df

        return df
