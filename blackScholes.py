# -*- coding: utf-8 -*-

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def d1(s, k, r, q, v, t):
    return (np.log(s / k) + (r - q + 0.5 * v * v) * t) / (v * np.sqrt(t))

def d2(s, k, r, q, v, t):
    return d1(s, k, r, q, v, t) - v * np.sqrt(t)

def callPutSign(optionType):
    if optionType[0].upper() == 'C':
        return 1.0
    else:
        return -1.0

def blackScholesPrice(optionType, s, k, r, q, v, t):
    cp = callPutSign(optionType)
    nd1 = norm.cdf(cp * d1(s, k, r, q, v, t))
    nd2 = norm.cdf(cp * d2(s, k, r, q, v, t))
    forward = s * np.exp((r - q)* t)
    discount = np.exp(-1.0 * r * t)
    return cp * discount * (forward * nd1 - k * nd2)

def blackScholesDelta(optionType, s, k, r, q, v, t):
    cp = callPutSign(optionType)
    nd1 = norm.cdf(cp * d1(s, k, r, q, v, t))
    return cp * np.exp(-1.0 * q * t) * nd1

def blackScholesGamma(optionType, s, k, r, q, v, t):
    return np.exp(-1.0 * q * t) * norm.pdf(d1(s, k, r, q, v, t)) / (s * v * np.sqrt(t))

def blackScholesVega(optionType, s, k, r, q, v, t):
    return s * np.exp(-1.0 * q * t) * norm.pdf(d1(s, k, r, q, v, t)) * np.sqrt(t)

def blackScholesVolga(optionType, s, k, r, q, v, t):
    vega = blackScholesVega(optionType, s, k, r, q, v, t)
    return vega * d1(s, k, r, q, v, t) * d2(s, k, r, q, v, t) / v

def blackScholes(optionType, s, k, r, q, v, t):
    price = blackScholesPrice(optionType, s, k, r, q, v, t)
    delta = blackScholesDelta(optionType, s, k, r, q, v, t)
    gamma = blackScholesGamma(optionType, s, k, r, q, v, t)
    vega = blackScholesVega(optionType, s, k, r, q, v, t)
    volga = blackScholesVolga(optionType, s, k, r, q, v, t)
    return {'price' : price,
            'delta' : delta,
            'gamma' : gamma,
            'vega' : vega,
            'volga' : volga}

def main():
    # prepare trades
    # [optionType, Spot, Strike, Risk free yield, Dividend yield, Volatiltiy, Time to expiry]
    oc = ['call', 100, 110, 0, 0, 0.1, 1]
    ac = ['call', 100, 100, 0, 0, 0.1, 1]
    ic = ['call', 100, 90, 0, 0, 0.1, 1]
    ip = ['put', 100, 90, 0, 0, 0.1, 1]
    ap = ['put', 100, 100, 0, 0, 0.1, 1]
    op = ['put', 100, 110, 0, 0, 0.1, 1]
    trades = [oc, ac, ic, ip, ap, op]
    # list of functions to call
    functions = [blackScholesPrice,
                 blackScholesDelta, blackScholesGamma,
                 blackScholesVega, blackScholesVolga]
    # 
    for tr in trades:
        for func in functions:
            print(func(tr[0], tr[1], tr[2], tr[3], tr[4], tr[5], tr[6]))
            pass
    #
    for tr in trades:
        print(blackScholes(tr[0], tr[1], tr[2], tr[3], tr[4], tr[5], tr[6]))
        pass

    spots = range(50, 151)
    results = []
    for spot in spots:
        results.append(blackScholes(ac[0], spot, ac[2], ac[3], ac[4], ac[5], ac[6]))

    fig = plt.figure()
    ax1 = fig.add_subplot(3, 2, 1)
    ax1.scatter(spots, [result.get('price') for result in results])
    ax1.set_title('Price')
    ax2 = fig.add_subplot(3, 2, 2)
    ax2.scatter(spots, [result.get('delta') for result in results])
    ax2.set_title('Delta')
    ax3 = fig.add_subplot(3, 2, 3)
    ax3.scatter(spots, [result.get('gamma') for result in results])
    ax3.set_title('Gamma')
    ax4 = fig.add_subplot(3, 2, 4)
    ax4.scatter(spots, [result.get('vega') for result in results])
    ax4.set_title('Vega')
    ax5 = fig.add_subplot(3, 2, 5)
    ax5.scatter(spots, [result.get('volga') for result in results])
    ax5.set_title('Volga')

if __name__ == "__main__":
    main()