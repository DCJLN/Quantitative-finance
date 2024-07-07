import pandas as pd
import yfinance as yf
from technical_indicator import TechnicalIndicator
from invest_bot import InvestBot


def main():
    # Parameters
    HIST_PERIOD = '3y'
    INTERVAL = '1d'
    TICKER = "^GSPC"
    # TICKER = "CSPX.L"

    # Downloading financial data
    data = yf.download(tickers=TICKER, period=HIST_PERIOD, interval=INTERVAL)

    # Cleaning and formatting data
    data = data.fillna(method='ffill')
    data.dropna(inplace=True)

    # Parameters
    parameters = {
        'rolling_days': 20,
        'std_factor': 2,
    }

    # Creating the investment bot
    inv_bot = InvestBot(fin_data=data)

    bb_out_up_signals = inv_bot.bb_out_up_strategy(parameters=parameters)
    inv_bot.back_testing(bb_out_up_signals)
    inv_bot.signal_visualization(bb_out_up_signals)

    first_d_m_signals = inv_bot.first_day_month_strategy()
    inv_bot.back_testing(first_d_m_signals)


if __name__ == '__main__':
    main()
