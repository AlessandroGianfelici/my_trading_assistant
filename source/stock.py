import yfinance as yf
import numpy as np


class Stock:
    def __init__(self, code: str, name: str = None):
        self.code = code
        self.name = name or code
        self.ticker = yf.Ticker(code)
        self.hist = self.ticker.history(period="max")
        self.hist['returns'] = (self.hist['Close'] - self.hist['Open'])/self.hist['Open']

        self._sigma = None
        self._financials = None
        self._balance_sheet = None
        
    @property
    def financials(self):
        self._financials = self._financials or self.ticker.financials.T.sort_index()
        return self._financials

    @property
    def balance_sheet(self):
        self._balance_sheet = self._balance_sheet or self.ticker.balance_sheet.T.sort_index()
        return self._balance_sheet

    @property
    def sigma(self):
        self._sigma = self._sigma or np.std(self.hist['returns'])
        return self._sigma

    
            