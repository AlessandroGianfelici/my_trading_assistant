import numpy as np

class Portfolio:
    def __init__(self, composition: dict, stocks : list):
        self.composition = composition
        self.hist = sum(map(lambda stock: composition[stock.name]*stock.hist, stocks)).dropna()
        self.hist['returns'] = (self.hist['Close'] - self.hist['Open'])/self.hist['Open']
        self.sigma = np.std(self.hist['returns'])      