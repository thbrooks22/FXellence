from forex_helpers import *
from datetime import date


def main():
    d = date(2007,11,1)
    d2 = date(2009, 1, 1)
    plot_rates_in_range(["AUD", "EUR", "GBP"], ["USD", "USD", "USD"], d, end=d2, sma=100)


if __name__ == '__main__':
    main()
