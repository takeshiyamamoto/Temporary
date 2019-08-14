# -*- coding: utf-8 -*-
#%%
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

#%%
def main():
    #%%
    # settings
    var_window = 250
    #%%
    # read data series
    price = pd.read_csv('MUFG.csv', index_col='Date')
    returns = price['Adj Close'].pct_change()
    returns.name = 'daily return'
    # calculate VaRs
    var_pos = returns.rolling(window=var_window).quantile(0.99)
    var_pos.name = '1% HS VaR'
    var_neg = returns.rolling(window=var_window).quantile(0.01)
    var_neg.name = '99% HS VaR'
    var_std = -1 * returns.rolling(window=var_window).std() * norm.ppf(0.99)
    var_std.name = '99% VC VaR'
    var_df = pd.concat([returns, var_pos, var_neg, var_std], axis=1)
    var_df.plot()
    plt.show()
    #%%
    # count outliers
    outliers_pos = np.where(var_pos[var_window:] - returns[var_window:].shift(-1) < 0, 1, 0)
    outliers_neg = np.where(var_neg[var_window:] - returns[var_window:].shift(-1) > 0, 1, 0)
    # cumulative sum of outliers
    sum_pos = pd.Series(outliers_pos).rolling(window=var_window).sum()
    sum_pos.index = returns.index[var_window:]
    sum_pos.name = 'Sum Outliers 1%'
    sum_neg = pd.Series(outliers_neg).rolling(window=var_window).sum()
    sum_neg.index = returns.index[var_window:]
    sum_neg.name = 'Sum Outliers 99%'
    sum_df = pd.concat([sum_pos, sum_neg], axis=1)
    sum_df.plot()
    plt.show()
    
#%%
if __name__ == "__main__":
    main()

#%%
