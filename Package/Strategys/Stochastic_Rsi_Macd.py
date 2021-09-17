from pandas.core.frame import DataFrame
import numpy as np
import pandas as pd
from Strategys.strategy import Strategy
import ta
class Stochastic_RSI_MACD(Strategy):
    def __get_triggers(self, df:DataFrame, lags:int, buy=True)->DataFrame:
        dfx = pd.DataFrame()
        for i in range(1, lags+1):
            if buy:
                mask = (df['%K'].shift(i) < 20) & (df['%D'].shift(i) < 20)
            else:
                mask = (df['%K'].shift(i) > 80) & (df['%D'].shift(i) > 80)
            dfx = dfx.append(mask, ignore_index=True)
        return dfx.sum(axis=0)

    def __generate_indicators(self, df:DataFrame)->DataFrame:
        df['%K'] = ta.momentum.stoch(df.High, df.Low, df.Close, window=14, smooth_window=3)
        df['%D'] = df['%K'].rolling(3).mean()
        df['rsi'] = ta.momentum.rsi(df.Close, window=14)
        df['macd'] = ta.trend.macd_diff(df.Close)
        df.dropna(inplace=True)
        df['Buytrigger'] = np.where(self.__get_triggers(df, 4),1,0)
        df['Selltrigger'] = np.where(self.__get_triggers(df,4, False),1,0)
        df['Buy'] = np.where((df.Buytrigger) & (df['%K'].between(20,80)) & (df['%D'].between(20,80)) & (df.rsi > 50) & (df.macd > 0), 1, 0)
        df['Sell'] = np.where((df.Selltrigger) & (df['%K'].between(20,80)) & (df['%D'].between(20,80)) & (df.rsi < 50) & (df.macd < 0), 1, 0)
        return df

    def __define_order_dates(self, df:DataFrame)->DataFrame:
        Buying_dates, Selling_dates = [],[]
        for i in range(len(df) - 1):
            if df.Buy.iloc[i]:
                Buying_dates.append(df.iloc[i+1].name)
                for num,j in enumerate(df.Sell[i:]):
                    if j:
                        Selling_dates.append(df.iloc[i + num + 1].name)
                        break

        cutit = len(Buying_dates) - len(Selling_dates)
        if cutit:
            Buying_dates = Buying_dates[:-cutit]

        frame = pd.DataFrame({'Buying_dates':Buying_dates, 'Selling_dates':Selling_dates})
        actuals = frame[frame.Buying_dates > frame.Selling_dates.shift(1)] #Don think the order should be opend and closed this way
        return actuals

    @property
    def execute(self):
        data_indicators = self.__generate_indicators(self.df)
        order_dates =  self.__define_order_dates(data_indicators)
        return order_dates
