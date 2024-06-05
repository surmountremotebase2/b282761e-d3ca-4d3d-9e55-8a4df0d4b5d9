from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the tickers to trade
        self.tickers = ["AAPL", "MSFT"]

    @property
    def assets(self):
        # Specify the assets the strategy will trade
        return self.tickers

    @property
    def interval(self):
        # Define the data interval (daily for this strategy)
        return "1day"

    @property
    def data(self):
        # Define the data required for the strategy
        # We only need OHLCV data for the tickers defined
        return [OHLCV(ticker) for ticker in self.tickers]

    def run(self, data):
        # Initialize allocation dictionary with zero allocations
        allocation_dict = {ticker: 0 for ticker in self.tickers}

        # Analyze data for each asset to determine buy or sell signals
        for ticker in self.tickers:
            ohlcv = data["ohlcv"][ticker]

            # Ensure there is enough data to analyze
            if len(ohlcv) < 20:
                continue

            # Calculate simple moving averages for trend identification
            sma_short = SMA(ticker, ohlcv, 5)
            sma_long = SMA(ticker, ohlcv, 20)

            # Check if there's a bullish crossover (SMA short crosses above SMA long)
            if sma_short[-1] > sma_long[-1] and sma_short[-2] < sma_long[-2]:
                log(f"Bullish crossover detected for {ticker}. Buying.")
                allocation_dict[ticker] = 0.5  # Allocate 50% of portfolio to this asset

            # Check if there's a bearish crossover (SMA short crosses below SMA long)
            elif sma_short[-1] < sma_long[-1] and sma_short[-2] > sma_long[-2]:
                log(f"Bearish crossover detected for {ticker}. Selling.")
                allocation_dict[ticker] = -0.5  # Allocate -50% for shorting (if short-selling is allowed)

        # Return a TargetAllocation object with the allocation dictionary
        return TargetAllocation(allocation_dict)