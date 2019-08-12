# -*- coding: utf-8 -*-
#%%
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

#%%
def main():
    # settings
    var_window = 250
    # read data series
    price = pd.read_csv('MUFG.csv', index_col='Date')
    returns = price['Adj Close'].pct_change()
    returns.plot()
    plt.show()
    # calculate VaRs
    ret_pos = returns.rolling(window=var_window).quantile(0.99)
    ret_neg = returns.rolling(window=var_window).quantile(0.01)
    ret_std = returns.rolling(window=var_window).std() * norm.ppf(0.99)
    ret_pos.plot()
    ret_neg.plot()
    ret_std.plot()
    plt.show()
    # count outliers
    outliers_pos = np.where(ret_pos[var_window:] - returns[var_window:] < 0, 1, 0)
    outliers_neg = np.where(ret_neg[var_window:] - returns[var_window:] > 0, 1, 0)
    sum_pos = pd.DataFrame(outliers_pos).rolling(window=var_window).sum()
    sum_neg = pd.DataFrame(outliers_neg).rolling(window=var_window).sum()
    sum_pos.plot()
    sum_neg.plot()
    plt.show()

#%%
if __name__ == "__main__":
    main()