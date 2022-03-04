import yfinance as yf
import numpy as np

#https://mrjbq7.github.io/ta-lib/

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
        if self._financials is None:
            self._financials = self.ticker.financials.T.sort_index()
        return self._financials

    @property
    def balance_sheet(self):
        if self._balance_sheet is None:
            self._balance_sheet = self.ticker.balance_sheet.T.sort_index()
        return self._balance_sheet

    @property
    def sigma(self):
        self._sigma = self._sigma or np.std(self.hist['returns'])
        return self._sigma            