from .price_fetcher import PriceFetcher
from .candle_builder import CandleBuilder

class datamanager:
    def __init__(self):
        self.fetcher = PriceFetcher()
        self.builder = CandleBuilder()

    def get_candles(self, symbol: str, interval: str, limit: int = None, market: str = "futures"):
        if limit is None:
            limit = self.fetcher.MAX_CANDLE_COUNTS.get(interval, 500)
        raw_data = self.fetcher.fetch(symbol, interval, limit, market)
        return self.builder.build(raw_data)
