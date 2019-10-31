import sys
sys.path.append('../backtesting')
from backtesting import Ruleset, Backtester, Portfolio
from forex_helpers import rates_in_range, sma, bollinger
from datetime import date, timedelta


def bollinger_bounce_test(portfolio, day):
    rate = rates_in_range("GBP", "USD", day, day)["rate"][0]
    rates, upper_bol_rate = bollinger("GBP", "USD", day, 50)
    _, lower_bol_rate = bollinger(None, None, None, None, upper=False, rates=rates)
    if (rate > upper_bol_rate):
        portfolio.transfer("USD", "GBP", self.sheet["USD"], rate)
    elif (rate < lower_bol_rate):
        portfolio.transfer("GBP", "USD", self.sheet["GBP"], (1 / rate))
    print(portfolio.sheet, flush=True)
    return portfolio


def main():
    R = Ruleset({"bbt" : bollinger_bounce_test})
    P = Portfolio({"USD" : 10000, "GBP" : 10000})
    B = Backtester(R)
    B.execute(P, date.today() - timedelta(100))


if __name__ == '__main__':
    main()
