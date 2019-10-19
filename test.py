from forex import *
from datetime import date


def main():
    d = date(2018,6,1)
    plot_rates_in_range(["USD", "USD", "USD"], ["GBP", "AUD", "CHF"], d, sma=100)


if __name__ == '__main__':
    main()
