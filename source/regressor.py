import pandas as pd
import os
from source.stock import Stock
from source.functions import plot_candle
import numpy as np
import matplotlib.pyplot as plt
import piecewise_regression
from datetime import datetime
from sklearn.linear_model import RANSACRegressor

class Regressor:
    def __init__(self, stock):

        self.stock = stock
        self._x = None
        self._y = None
        self.model = None

    @property
    def x(self):
        if self._x is None:
            self._x = (1/365)*(pd.Series(self.stock.hist.index - datetime.today()).dt.days).values
        return self._x

    @property
    def y(self):
        if self._y is None:
            self._y = self.stock.hist['Close'].apply(np.log).values
        return self._y

    def get_breakpoint(self):
        breakpoint1 = self.model.get_results()['estimates']['breakpoint1']
        return (datetime.today() + pd.Timedelta(days=365*breakpoint1['estimate']))

    def fit_trend_with_changepoints(self, n_breakpoints):
        self.model = piecewise_regression.Fit(self.x, self.y, n_breakpoints=n_breakpoints)
        return self.model

    def predict(self, x = None):
        x = x or self.x
        return np.exp(self.predict(x))

    def fit_ransac(self):
        self.ransac_model = RANSACRegressor()
        self.ransac_model.fit(self.x.reshape(-1, 1), self.y.reshape(-1, 1))
        return self.ransac_model

    def predict_ransac(self, days_from_today = np.array([1/365]).reshape(1, -1)):
        return np.exp(self.ransac_model.predict(days_from_today))

    def predict(self, xx_plot):
        """
        Predict using a trained Muggeo's model.
        """
        if not self.model.best_muggeo:
            print("Algorithm didn't converge. No fit to plot.")
        else:
            # Get the final results from the fitted model variables
            # Params are in terms of [intercept, alpha, betas, gammas]
            final_params = self.model.best_muggeo.best_fit.raw_params
            breakpoints = self.model.best_muggeo.best_fit.next_breakpoints
            # Extract what we need from params etc
            intercept_hat = final_params[0]
            alpha_hat = final_params[1]
            beta_hats = final_params[2:2 + len(breakpoints)]
    
            # Build the fit plot segment by segment. Betas are defined as
            # difference in gradient from previous section
            yy_plot = intercept_hat + alpha_hat * xx_plot
            for bp_count in range(len(breakpoints)):
                yy_plot += beta_hats[bp_count] * \
                    np.maximum(xx_plot - breakpoints[bp_count], 0)
            return yy_plot


