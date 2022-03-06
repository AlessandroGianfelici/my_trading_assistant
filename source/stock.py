import yfinance as yf
import numpy as np
import pandas as pd
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
        self._open_positions = None
        self._full_time_employees = None

    @property
    def open_positions(self):
        if self._open_positions is None:
            self._open_positions = pd.read_csv("open_positions.csv", index_col =0)
            self._open_positions.loc[self._open_positions.index == self.code].reset_index(drop=1)
        return self._open_positions[['open_jobs', 'YYYYMM']]

    @property
    def info(self):
        if self._info is None:
            self._info = self.ticker.info
        return self._info
        

    @property
    def full_time_employees(self):
        if self._full_time_employees is None:
            try:
                self._full_time_employees = self.info['fullTimeEmployees']
            except:
                self._full_time_employees = self._open_positions['tot_employees'][0]
        return self._full_time_employees

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

    @property
    def dividends(self):
        return self.hist['Dividends'].replace({0:None}).dropna()