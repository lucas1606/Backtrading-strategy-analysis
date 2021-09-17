from pandas.core.frame import DataFrame
from abc import ABC, abstractmethod
class Strategy(ABC):
    """
    Basic struture for any trading strategy
    """   
    def __init__(self, df:DataFrame=None)->None:
        self._df = df
        if self._df:
            self.execute
               
    @property    
    def df(self):
        return self._df
    
    @df.setter
    def df(self,df):
        self._df = df

    @abstractmethod
    def execute(self):
        pass