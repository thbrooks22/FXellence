import numpy as np
import pandas as pd
import calendar
from scipy import stats
from matplotlib import dates
from matplotlib import pyplot as plt
from matplotlib import axes
from datetime import *
from forex_python.converter import CurrencyRates as C

c = C()
pd.plotting.register_matplotlib_converters()


def rates_in_range(to_cur, from_cur, start, end=date.today()):
    dates = [start + timedelta(i) for i in \
        range((end - start + timedelta(1)).days)]
    rates = [c.get_rate(from_cur, to_cur, date) for date in dates]
    table = pd.DataFrame(rates, index=dates)
    table.columns = ["rate"]
    return table


#-------------------------------------------------------------------------------
#---------------------------------- Plotting -----------------------------------
#-------------------------------------------------------------------------------

def plot_time_series(x_data, y_data, param_dict):
    x_len = len(x_data)
    y_len = len(y_data)
    if x_len != y_len or y_len != len(param_dict):
        raise ValueError("Data size mismatch.")
    fig = plt.figure()
    sqrtx_len = np.sqrt(x_len)
    if int(sqrtx_len) == sqrtx_len:
        n_rows, n_cols = sqrtx_len, sqrtx_len
    else:
        n_rows, n_cols = int(sqrtx_len) + 1, int(sqrtx_len) + 1
    for i in range(x_len):
        ax = fig.add_subplot(n_rows, n_cols, i+1, **(param_dict[i]))
        ax.plot(x_data[i], y_data[i])
        ax.grid(which='both', axis='both')
        plt.xticks(rotation=30, size='x-small')
    plt.subplots_adjust(wspace=0.5, hspace=0.5)


def plot_seasonal_trend(to_cur, from_cur, month, start_year, \
    end_year=date.today().year):
    y_pos = range(0, end_year - start_year + 1)
    years = range(start_year, end_year + 1)
    dates = [[date(yr, month, 1), date(yr, month, calendar.monthrange(yr, month)[1])] \
                for yr in years]
    shifts = [(c.get_rate(to_cur, from_cur, dates[i][1]) - \
        c.get_rate(to_cur, from_cur, dates[i][0])) / \
        c.get_rate(to_cur, from_cur, dates[i][0]) * 100 for i in \
        y_pos]
    plt.bar(y_pos, shifts, align='center', alpha=0.5, color="black")
    plt.xlabel("date", c="blue")
    plt.ylabel("monthly change in exchange rate", c="blue")
    plt.title(from_cur + "/" + to_cur + ", monthly change in exchange rate, " + \
        ("%d-%d" % (month, start_year)) + " to " + ("%d-%d" % (month, end_year)))
    plt.xticks(y_pos, ["%d,\n%.2f%%" % (years[i], shifts[i]) for i in y_pos])
    plt.show()


def plot_rate_comparison(pair1, pair2, start, end=date.today()):
    to1, from1 = pair1
    to2, from2 = pair2
    rates1 = rates_in_range(to1, from1, start, end)
    rates2 = rates_in_range(to2, from2, start, end)
    slope, intercept, r_value, p_value, std_err = \
        stats.linregress(rates1["rate"], rates2["rate"])
    line = slope * rates1["rate"] + intercept
    plt.plot(rates1["rate"], rates2["rate"], 'o')
    regression, = plt.plot(rates1["rate"], line)
    plt.legend([regression], \
        ["y = %f*x + %f\nr = %f" % (slope, intercept, r_value)])
    plt.title(from2 + "/" + to2 + " vs. " + from1 + "/" + to1 + ", " + \
        rates1.index[0].strftime("%m-%d-%Y") + " to " + \
        rates1.index[-1].strftime("%m-%d-%Y"))
    plt.xlabel(from1 + "/" + to1, c="blue")
    plt.ylabel(from2 + "/" + to2, c="blue")
    plt.show()


def plot_rates_in_range(to_curs, from_curs, start, end=date.today()):
    to_curs_len = len(to_curs)
    if to_curs_len != len(from_curs):
        raise ValueError("Data size mismatch.")
    rate_sheet, param_dict = [], []
    for i in range(to_curs_len):
        rate_sheet.append(rates_in_range(to_curs[i], from_curs[i], start, end))
        param_dict.append({
            'title' : from_curs[i] + "/" + to_curs[i] + ", " + \
                rate_sheet[i].index[0].strftime("%m-%d-%Y") + " to " + \
                rate_sheet[i].index[-1].strftime("%m-%d-%Y"),
            'xlabel' : "date",
            'ylabel' : "exchange rate"
        })
    plot_time_series([rs.index for rs in rate_sheet], [rs["rate"] for rs in rate_sheet], \
        param_dict)
    plt.show()
