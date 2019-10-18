from forex import *
from datetime import date


def main():
    d = date(2019,1,1)
    plot_rates_in_range(["USD", "USD", "USD", "USD"], ["CHF", "GBP", "JPY", "AUD"], \
        d, sma=50)


if __name__ == '__main__':
    main()
