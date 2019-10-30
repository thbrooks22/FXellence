import sys
sys.path.append('../backtesting')
from backtesting import Ruleset, Backtester, Portfolio
from forex_helpers import rates_in_range, sma, bollinger
from datetime import date, timedelta


def bollinger_bounce_test(portfolio, day):
    rate = rates_in_range("GBP", "USD", day, day)["rate"][0]
    if (rate > bollinger("GBP", "USD", day, 50)):
        portfolio.update("GBP", portfolio.sheet["GBP"] + rate * \
            portfolio.sheet["USD"])
        portfolio.update("USD", 0)
    elif (rate < bollinger("GBP", "USD", day, 50, \
        upper=False)):
        portfolio.update("USD", portfolio.sheet["USD"] + (1 / rate) * \
            portfolio.sheet["GBP"])
        portfolio.update("GBP", 0)
    print(portfolio.sheet, flush=True)
    return portfolio


def main():
    R = Ruleset({"bbt" : bollinger_bounce_test})
    P = Portfolio({"USD" : 10000, "GBP" : 10000})
    B = Backtester(R)
    B.execute(P, date.today() - timedelta(100))


if __name__ == '__main__':
    main()
