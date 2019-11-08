import sys
sys.path.append('../backtesting')
sys.path.append('../helpers')
from backtesting import Ruleset, Backtester, Portfolio
from forex_helpers import rates_in_range, sma, bollinger
from datetime import date, timedelta


def bollinger_bounce_test(portfolio, day, memo, pairs):
    for pair in pairs:
        pair_name = pair["frm"] + "/" + pair["to"]
        rate = rates_in_range(pair["to"], pair["frm"], day, day)["rate"][0]
        if pair_name not in memo or memo[pair_name] is None:
            memo[pair_name], upper_bol_rate = bollinger(pair["to"], pair["frm"], \
                day, 100)
            memo[pair_name] = list(memo[pair_name])
        else:
            memo[pair_name], upper_bol_rate = bollinger(None, None, None, None, \
                rates=memo[pair_name][1:] + [rate])
        _, lower_bol_rate = bollinger(None, None, None, None, upper=False, \
            rates=memo[pair_name])
        if (rate > upper_bol_rate):
            portfolio.transfer(pair["frm"], pair["to"], portfolio.sheet[pair["frm"]], \
                rate)
        elif (rate < lower_bol_rate):
            portfolio.transfer(pair["to"], pair["frm"], portfolio.sheet[pair["to"]], \
                (1 / rate))
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
