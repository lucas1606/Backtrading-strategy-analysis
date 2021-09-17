from .test import Test
from Strategys.strategy import Strategy

class UnitTest(Test):
    def __init__(self, ticker:str, strategy:Strategy , past_days:int=59, interval:str='30m')->None:

        self._ticker = ticker
        self.past_days = past_days
        self.interval = interval
        super().__init__(strategy)
    
    @property
    def ticker(self):
        return self._ticker

    @property
    def execute(self):
        df = self.get_data(self.ticker, self.past_days, self.interval)
        order_dates = self.apply_strategy(df, self.strategy)
        profit = self.calculate_profit(df, order_dates)
        self.plot_graph(df ,order_dates)      
        return profit

class MultipleActionTest(UnitTest):

    def __init__(self, ticker_list:list, strategy:Strategy , past_days:int=59, interval:str='30m')->None:
        self._ticker_list = ticker_list
        self._strategy = strategy
        self.past_days = past_days
        self.interval = interval
        

    @property
    def ticker_list(self):
        return self._ticker_list

    @property
    def execute(self):
        profit_list = []
        for ticker in self.ticker_list:
            df = self.get_data(ticker, self.past_days, self.interval)
            order_dates = self.apply_strategy(df, self.strategy)
            profit = self.calculate_profit(df, order_dates)
            profit_list.append(tuple((ticker,profit)))
        return profit_list