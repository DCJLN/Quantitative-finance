import pandas as pd
import yfinance as yf
from technical_indicator import TechnicalIndicator
from invest_bot import InvestBot


def main():
    # Parameters
    HIST_PERIOD = '1y'
    INTERVAL = '1d'
    TICKER = "^GSPC"
    # TICKER = "CSPX.L"

    # Downloading financial data
    data = yf.download(tickers=TICKER, period=HIST_PERIOD, interval=INTERVAL)

    # Cleaning and formatting data
    data = data.fillna(method='ffill')
    data.dropna(inplace=True)
    # data['Adj Close_-1'] = data['Adj Close'].shift(1)

    # Parameters
    parameters = {
        'rolling_days': 20,
        'std_factor': 2,
    }

    # Creating the investment bot
    inv_bot = InvestBot(fin_data=data)

    inv_bot.bb_out_up_strategy(parameters=parameters)
    inv_bot.back_testing()

    inv_bot.first_day_month_strategy()
    inv_bot.back_testing()


if __name__ == '__main__':
    main()
