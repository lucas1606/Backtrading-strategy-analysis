from pandas.core.frame import DataFrame
from abc import ABC, abstractmethod
from Strategys.strategy import Strategy
import datetime
import yfinance as yf
import matplotlib.pyplot as plt


class Test(ABC):

    def __init__(self, strategy:Strategy, **kargs):
        self._strategy = strategy

    @property
    def strategy(self)-> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy:Strategy)-> None:
        if type(strategy) is Strategy:
            self._strategy = strategy
        else:
            return TypeError

    def get_data(self, ticker:str, past_days = 59, interval = '30m') -> DataFrame :
        '''
        get_data function recives any active ticker (according to the yahoo finance nomeclature),
        the past days os data, and the data interval.
        '''
        start_date = str(datetime.date.today() - datetime.timedelta(past_days))
        df = yf.download(ticker, start=start_date, interval=interval, progress=False)
        return df

    def apply_strategy(self, df:DataFrame, strategy:Strategy)->DataFrame:
        strategy.df = df
        order_dates =  strategy.execute
        return order_dates
        
    def calculate_profit(self, df:DataFrame, order_dates):
        Buyprices = df.loc[order_dates.Buying_dates].Open
        Sellprices = df.loc[order_dates.Selling_dates].Open
        profits = (Sellprices.values - Buyprices.values)/Buyprices.values
        return profits.mean()*100
        
    def plot_graph(self, df:DataFrame, actuals:DataFrame):
        plt.figure(figsize=(40,20))
        plt.subplot(511)
        plt.plot(df.Close, color='k', alpha=0.7)
        #plt.plot(df['rsi']/50, alpha= 0.5)
        plt.scatter(actuals.Buying_dates, df.Open[actuals.Buying_dates], marker='^', color='g', s=500)
        plt.scatter(actuals.Selling_dates, df.Open[actuals.Selling_dates], marker='v', color='r', s=500)
        plt.subplot(512)
        plt.plot(df['rsi'], color='b', alpha=0.8)
        plt.subplot(513)
        plt.plot(df['%K'], color='g', alpha=0.5)
        plt.subplot(514)
        plt.plot(df['%D'], color='y', alpha=0.5)
        plt.subplot(515)
        plt.plot(df['macd'], color='m', alpha=0.5)

    @abstractmethod
    def execute(self):
        pass