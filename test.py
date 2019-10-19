from forex import *
from datetime import date


def main():
    d = date(2016,1,1)
    plot_rates_in_range(["USD"], ["GBP"], \
        d, sma=50)


if __name__ == '__main__':
    main()
