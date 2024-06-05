from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers this strategy will trade
        self.tickers = ["AAPL", "MSFT", "GOOGL"]
    
    @property
    def interval(self):
        # Setting the interval for data aggregation (e.g., "1day" for daily data)
        return "1day"
    
    @property
    def assets(self):
        # Defining the assets that this strategy will trade
        return self.tickers
    
    @property
    def data(self):
        # No additional data required for this strategy beyond price
        return []
    
    def detect_chart_pattern(self, data):
        """
        This function detects simple chart patterns in the price data.
        It's a placeholder for more complex logic.
        
        Arguments:
            data: The price data for the asset
        
        Returns:
            direction: The expected direction of the price movement ("bullish", "bearish", or "neutral")
        """
        # Example: Detecting a bullish crossover
        close_prices = [i['close'] for i in data]
        short_term_sma = SMA(close_prices, length=5)
        long_term_sma = SMA(close_prices, length=20)
        
        if short_term_sma[-1] > long_term_sma[-1] and short_term_sma[-2] <= long_term_sma[-2]:
            return "bullish"
        elif short_term_sma[-1] < long_term_sma[-1] and short_term_sma[-2] >= long_term_sma[-2]:
            return "bearish"
        else:
            return "neutral"
    
    def run(self, data):
        allocation_dict = {}
        
        # Loop through each ticker to decide on the allocation based on detected chart patterns
        for ticker in self.tickers:
            ohlcv_data = data["ohlcv"][ticker]
            pattern_direction = self.detect_chart_pattern(ohlcv_data)
            
            if pattern_direction == "bullish":
                # Strategy is bullish, so we allocate 100% to this asset
                allocation_dict[ticker] = 1.0 / len(self.tickers)
            elif pattern_direction == "bearish":
                # Strategy is bearish, but as an example, we do not short and hence allocate 0
                allocation_dict[ticker] = 0
            else:
                # Neutral view, equally distribute across assets without strong signals
                allocation_dict[ticker] = 1.0 / len(self.tickers)
        
        # Normalize allocations to ensure they sum up to 1 (or less)
        total_allocation = sum(allocation_dict.values())
        for ticker in allocation_dict:
            allocation_dict[ticker] /= total_allocation
        
        return TargetAllocation(allocation_dict)