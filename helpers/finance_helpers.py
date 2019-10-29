import numpy as np
import pandas as pd
import math
from scipy import stats as st

# ********************************************************
# --------------- Basic financial formulae ---------------
# ********************************************************

"""
simple_return : simple return on investment for a single financial asset between
    time t-1 and time t (optionally with dividend paid)

Args
old_price (float) : price of asset at time t-1
new_price (float) : price of the same asset at time t
(opt) dividend (float) : dividend paid to investor between time t-1 and time t
"""
def simple_return(old_price, new_price, dividend=0):
    return (new_price + dividend) / old_price - 1


"""
simple_portfolio_return : simple return on investment for an investment
    portfolio between time t-1 and time t

Args
weights (np.ndarray) : relative weights of financial assets as part of a
    portfolio
returns (np.ndarray) : returns on financial assets between time t-1 and time t
"""
def simple_portfolio_return(weights, returns):
    if np.sum(weights) != 1:
        raise ValueError("Relative weights of portfolio assets must sum to 1")
    if len(weights) != len(returns):
        raise ValueError("Number of weights must match number of returns.")
    sum = 0
    for i in range(len(weights)):
        sum += weights[i] * returns[i]
    return sum


"""
compound_return : compound return on investment for a single financial asset
    between time t-k+1 and time t

Args
old_price (float) : price of asset at time t-k+1
new_price (float) : price of the same asset at time t
"""
def compound_return(old_price, new_price):
    return new_price / old_price + 1


"""
average_compound_return : per-period compound return on investment for a single
    financial asset between time t-k+1 and time t

Args
returns (np.ndarray) : returns on a single financial asset over multiple periods
"""
def average_compound_return(returns):
    num_periods = len(returns)
    product = 1
    for i in range(num_periods):
        product *= returns[i] + 1
    return product ** (1 / num_periods) - 1


"""
continuous_compound_return : continuously compounded return on investment for a
    single financial asset between time t-1 and time t

Args
rtrn (float) : simple return between time t-1 and time t
"""
def continuous_compound_return(rtrn):
    return math.log10(rtrn + 1)


"""
future_value : future value of a single financial asset as a function of its
    present value, the discount rate, and periods of compounding

Args
present_value (float) : present value of a financial asset
discount_rate (float) : rate of return on this financial asset per period
num_periods (int) : number of periods over which to compound value
"""
def future_value(present_value, discount_rate, num_periods):
    return present_value * (1 + discount_rate) ** num_periods


"""
present_value : present value of a single financial asset as a function of
    desired future value, the discount rate, and periods of compounding

Args
future_value (float) : desired or expected value of a financial asset in the
    future
discount_rate (float) : rate of return on this financial asset per period
num_periods (int) : number of periods over which to discount value
"""
def present_value(future_value, discount_rate, num_periods):
    return future_value / (1 + discount_rate) ** num_periods


"""
dcf_present_value : present value of a financial asset according to the dcf
    model between time t and time t+1

Args
expected_price (float) : expected price of a financial asset at time t+1
expected_return (float) : expected simple return on investment between time t
    and time t+1 (assumes constant returns)
(opt) dividend (float) : dividend paid to investor between time t and time t+1
"""
def dcf_present_value(expected_price, expected_return, dividend=0):
    return (expected_price + dividend) / (1 + expected_return)


"""
dcf_present_value : present value of a financial asset according to the dcf
    model between time t and time t+k

Args
expected_price (float) : expected price of a financial asset at time t+k
expected_return (float) : expected simple return on investment per period
    between time t and time t+k (assumes constant returns)
expected_dividends (np.ndarray) : expected dividends paid to investor per period
    between time t and time t+k
"""
def dcf_multi_present_value(expected_price, expected_return, expected_dividends):
    num_periods = len(expected_dividends)
    sum = 0
    for i in range(num_periods):
        sum += expected_dividends[i] / (1 + expected_return) ** (i + 1)
    return sum + expected_price / (1 + expected_return) ** num_periods
