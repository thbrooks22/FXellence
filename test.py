from forex import *
from datetime import date


def main():
    d = date(2019,1,1)
    plot_rates_in_range(["JPY", "GBP", "CHF"], ["USD", "USD", "USD"], d)


if __name__ == '__main__':
    main()
