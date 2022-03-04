import yfinance as yf
import numpy as np

#https://mrjbq7.github.io/ta-lib/

class Stock:
    def __init__(self, code: str, name: str = None):
        self.code = code
        self.name = name or code
        self.ticker = yf.Ticker(code)

        self._hist = None
        self._info = None
        self._sigma = None
        self._financials = None
        self._quarterly_financials = None
        self._balance_sheet = None
        self._forward_PE = None
        self._trailing_PE = None

    @property
    def info(self):
        if self._info is None:
            self._info = self.ticker.info
        return self._info
        

    @property
    def forward_PE(self):
        if self._forward_PE is None:
            self._forward_PE = self.info['forwardPE']
        return self._forward_PE
        
    @property
    def trailing_PE(self):
        if self._trailing_PE is None:
            self._trailing_PE = self.info['trailingPE']
        return self._trailing_PE

    @property
    def financials(self):
        if self._financials is None:
            self._financials = self.ticker.financials.T.sort_index()
        return self._financials

    @property
    def quarterly_financials(self):
        if self._quarterly_financials is None:
            self._quarterly_financials = self.ticker._quarterly_financials.T.sort_index()
        return self._quarterly_financials

    @property
    def balance_sheet(self):
        if self._balance_sheet is None:
            self._balance_sheet = self.ticker.balance_sheet.T.sort_index()
        return self._balance_sheet

    @property
    def sigma(self):
        self._sigma = self._sigma or np.std(self.hist['returns'])
        return self._sigma            

    @property
    def hist(self):
        if self._hist is None:
            self._hist = self.ticker.history(period="max")
            self._hist['returns'] = (self._hist['Close'] - self._hist['Open'])/self._hist['Open']
        return self._hist