import sys
sys.path.append('../backtesting')
sys.path.append('../helpers')

from forex_helpers import *
from datetime import date


def main():
    d = date(2017,6,1)
    plot_rates_in_range(["USD"], ["GBP"], d, sma=100)


if __name__ == '__main__':
    main()
