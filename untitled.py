# -*- coding: utf-8 -*-
#%%
import numpy as np
import pandas as pd

#%%
def main():
    s = 100.0
    r = 0.01
    q = 0.01
    v = 0.2
    t = 1.0
    trial = 1000000
    np.random.seed(0)
    z = np.random.standard_normal(trial)
    f = pd.DataFrame(s * np.exp((r - q - 0.5 * v ** 2) * t + v * np.sqrt(t) * z))
    pl = f - s
    print(pl)
    
    price = pd.read_csv('MUFG.csv', index_col='Date')
    returns = price['Adj Close'].pct_change()
    diffs = price['Adj Close'].diff()

    total_obs_days = returns.count()
    obs_days = 252 * 3
    for i in range(total_obs - obs_days):
        
    
    pass

def percentile()

#%%
if __name__ == "__main__":
    main()