from forex import *
from datetime import date


def main():
    d = date(2019,8,1)
    plot_rate_comparison([["USD", "GBP"], ["JPY", "USD"]], [["GBP", "CHF"], ["JPY", "CHF"]], d)


if __name__ == '__main__':
    main()
