import numpy as np
import pandas as pd
import calendar
from scipy import stats
from matplotlib import dates
from matplotlib import pyplot as plt
from matplotlib import axes
from datetime import date, timedelta
from forex_python.converter import CurrencyRates as C


c = C()
pd.plotting.register_matplotlib_converters()


"""
fun : string * string * datetime.date [* datetime.date] -> pd.DataFrame

Args:
to_cur : currency denominator
from_cur : currency numerator
start : start date
[end : end date]

Desc: returns pd.DataFrame of from_cur/to_cur as valued daily by ECB from start to
    end dates.
"""
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

"""
fun : datetime.date iter * float iter * dict [* float iter] -> ()

Args:
x_data : datetime.date iter of x-axis data
y_data : float iter of y-axis data
param_dict : dictionary of plot parameters
[sma_data : data to compute simple moving average]

Desc: shows plot of y_data values vs x_data date range with param_dict parameters
    applied.
"""
def plot_time_series(x_data, y_data, param_dict, sma_data=None):
    x_len = len(x_data)
    y_len = len(y_data)
    if x_len != y_len or y_len != len(param_dict):
        raise ValueError("Data size mismatch.")
    sqrtx_len = np.sqrt(x_len)
    if int(sqrtx_len) == sqrtx_len:
        n_rows, n_cols = sqrtx_len, sqrtx_len
    else:
        n_rows, n_cols = int(sqrtx_len) + 1, int(sqrtx_len) + 1
    fig = plt.figure()
    if sma_data is None:
        for i in range(x_len):
            ax = fig.add_subplot(n_rows, n_cols, i+1, **(param_dict[i]))
            ax.plot(x_data[i], y_data[i], color="black")
            ax.grid(which='both', axis='both')
            plt.xticks(rotation=30, size='x-small')
    else:
        sma, sma_sheet = sma_data
        l = len(x_data[0])
        for i in range(x_len):
            sma_plot = [np.mean(sma_sheet[i][j:sma+j]) for j in range(l)]
            upper_bol_plot = [np.mean(sma_sheet[i][j:sma+j]) + 2 * \
                np.std(sma_sheet[i][j:sma+j]) for j in range(l)]
            lower_bol_plot = [np.mean(sma_sheet[i][j:sma+j]) - 2 * \
                np.std(sma_sheet[i][j:sma+j]) for j in range(l)]
            ax = fig.add_subplot(n_rows, n_cols, i+1, **(param_dict[i]))
            ax.plot(x_data[i], y_data[i], color="black")
            ma, = ax.plot(x_data[i], sma_plot)
            upper_bol, = ax.plot(x_data[i], upper_bol_plot)
            lower_bol, = ax.plot(x_data[i], lower_bol_plot)
            ax.fill_between(x_data[i], lower_bol_plot, upper_bol_plot, color="grey")
            ax.legend((ma, upper_bol, lower_bol), ("%d day moving avg" % sma, \
                "upper band", "lower band"))
            ax.grid(which='both', axis='both')
            plt.xticks(rotation=30, size='x-small')
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()


"""
fun : float iter * float iter * dict * dict -> ()

Args:
x_data : float iter of x_axis data
y_data : float iter of y_axis data
linear_regression : dict of regression values slope, intercept, line, r_value
param_dict : dictionary of plot parameters

Desc: shows plot of scattered y_data vs x_data with linear regression line
    and r value and param_dict parameters applied.
"""
def plot_scatter(x_data, y_data, linear_regression, param_dict):
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
        ax.scatter(x_data[i], y_data[i])
        regression, = ax.plot(x_data[i], linear_regression[i]["line"])
        ax.legend([regression], \
            ["y = %f*x + %f\nr = %f" % (linear_regression[i]["slope"], \
            linear_regression[i]["intercept"], linear_regression[i]["r_value"])])
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()


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


"""
fun : (string iter) iter * (string iter) iter * datetime.date [* datetime.date]
    -> ()

Args:
x_rates_tf : iter of string pair (to, from) to be plotted against corresponding
    y-pairs
y_rates_tf : iter of string pair (to, from) to be plotted against corresponding
    x-pairs
start : start date
[end : end date]

Desc: shows multiplot of scatters of from/to on y-axis vs from/to on x-axis
    for different currency pairs with linear regression.
"""
def plot_rate_comparison(x_rates_tf, y_rates_tf, start, end=date.today()):
    x_len = len(x_rates_tf)
    if x_len != len(y_rates_tf):
        raise ValueError("Data size mismatch.")
    x_rate_sheet, y_rate_sheet, regression, param_dict = [], [], [], []
    for i in range(x_len):
        x_rate_sheet.append(rates_in_range(x_rates_tf[i][0], x_rates_tf[i][1], start, end))
        y_rate_sheet.append(rates_in_range(y_rates_tf[i][0], y_rates_tf[i][1], start, end))
        regression.append({})
        regression[i]["slope"], regression[i]["intercept"], regression[i]["r_value"], _, _ = \
            stats.linregress(x_rate_sheet[i]["rate"], y_rate_sheet[i]["rate"])
        regression[i]["line"] = regression[i]["slope"] * x_rate_sheet[i]["rate"] \
            + regression[i]["intercept"]
        param_dict.append({
            'title' : y_rates_tf[i][1] + "/" + y_rates_tf[i][0] + " vs. " + \
                x_rates_tf[i][1] + "/" + x_rates_tf[i][0] + ", " + \
                x_rate_sheet[i].index[0].strftime("%m-%d-%Y") + " to " + \
                x_rate_sheet[i].index[-1].strftime("%m-%d-%Y"),
            'xlabel' : x_rates_tf[i][1] + "/" + x_rates_tf[i][0],
            'ylabel' : y_rates_tf[i][1] + "/" + y_rates_tf[i][0]
        })
    plot_scatter([xrs["rate"] for xrs in x_rate_sheet], [yrs["rate"] for yrs in \
        y_rate_sheet], regression, param_dict)


"""
fun : string iter * string iter * datetime.date [* datetime.date] [* int] -> ()

Args:
to_curs : list of currency denominators
from_curs : list of currency numerators
start : start date
[end : end date]
[sma : days over which to calculate simple moving average]

Desc: shows multiplot of time series of from/to value from start to end, potentially
    displaying simple moving average and bollinger bands.
"""
def plot_rates_in_range(to_curs, from_curs, start, end=date.today(), sma=None):
    to_curs_len = len(to_curs)
    if to_curs_len != len(from_curs):
        raise ValueError("Data size mismatch.")
    rate_sheet, param_dict = [], []
    if sma is None:
        for i in range(to_curs_len):
            rate_sheet.append(rates_in_range(to_curs[i], from_curs[i], start, end))
            param_dict.append({
                'title' : from_curs[i] + "/" + to_curs[i] + ", " + \
                    rate_sheet[i].index[0].strftime("%m-%d-%Y") + " to " + \
                    rate_sheet[i].index[-1].strftime("%m-%d-%Y"),
                'xlabel' : "date",
                'ylabel' : "exchange rate"
            })
        plot_time_series([rs.index for rs in rate_sheet], [rs["rate"] for rs in \
            rate_sheet], param_dict)
    else:
        sma_sheet = [rates_in_range(to_curs[i], from_curs[i], start - timedelta(sma), \
            end) for i in range(to_curs_len)]
        for i in range(to_curs_len):
            rate_sheet.append(rates_in_range(to_curs[i], from_curs[i], start, end))
            param_dict.append({
                'title' : from_curs[i] + "/" + to_curs[i] + ", " + \
                    rate_sheet[i].index[0].strftime("%m-%d-%Y") + " to " + \
                    rate_sheet[i].index[-1].strftime("%m-%d-%Y"),
                'xlabel' : "date",
                'ylabel' : "exchange rate"
            })
        plot_time_series([rs.index for rs in rate_sheet], [rs["rate"] for rs in \
            rate_sheet], param_dict, (sma, [sms["rate"] for sms in sma_sheet]))


#-------------------------------------------------------------------------------
#--------------------------------- Technicals ----------------------------------
#-------------------------------------------------------------------------------

def sma(to_cur, from_cur, today, days, rates=None):
    if rates is None:
        rates = rates_in_range(to_cur, from_cur, today - timedelta(days),
            today)["rate"]
    return rates, np.mean(rates)


def bollinger(to_cur, from_cur, today, days, upper=True, rates=None):
    if rates is None:
        rates, sma_rates = sma(to_cur, from_cur, today, days)
    else:
        _, sma_rates = sma(None, None, None, None, rates)
    if upper:
        return rates, sma_rates + 2 * np.std(rates)
    return rates, sma_rates - 2 * np.std(rates)
