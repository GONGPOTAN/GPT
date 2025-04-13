# wsclient/utils/stream_builder.py
from config.symbols import get_all_symbols

def build_stream_url() -> str:
    all_symbols = get_all_symbols()
    streams = []
    for market_type, symbol_list in all_symbols.items():
        for symbol in symbol_list:
            streams.append(f"{symbol.lower()}@kline_1m")
    return f"wss://stream.binance.com:9443/stream?streams={'/'.join(streams)}"