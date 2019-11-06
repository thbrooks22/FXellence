import sys
sys.path.append('../backtesting')
sys.path.append('../helpers')
from backtesting import Ruleset, Backtester, Portfolio
from forex_helpers import rates_in_range, sma, bollinger
from datetime import date, timedelta


def bollinger_bounce_test(portfolio, day, memo):
    rate = rates_in_range("GBP", "USD", day, day)["rate"][0]
    if memo is None:
        memo, upper_bol_rate = bollinger("GBP", "USD", day, 100)
        memo = list(memo)
    else:
        memo, upper_bol_rate = bollinger(None, None, None, None, rates=memo[1:] + [rate])
    _, lower_bol_rate = bollinger(None, None, None, None, upper=False, rates=memo)
    if (rate > upper_bol_rate):
        portfolio.transfer("USD", "GBP", portfolio.sheet["USD"], rate)
    elif (rate < lower_bol_rate):
        portfolio.transfer("GBP", "USD", portfolio.sheet["GBP"], (1 / rate))
    print(day)
    print("RATE: " + str(rate))
    print("UPPER: " + str(upper_bol_rate))
    print("LOWER: " + str(lower_bol_rate))
    print(portfolio.sheet)
    return memo, portfolio


def main():
    R = Ruleset({"bbt" : bollinger_bounce_test})
    P = Portfolio({"USD" : 10000, "GBP" : 0})
    B = Backtester(R)
    B.execute(P, date.today() - timedelta(500))


if __name__ == '__main__':
    main()
