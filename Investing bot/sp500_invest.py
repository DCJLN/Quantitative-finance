import pandas as pd
import yfinance as yf
from technical_indicator import TechnicalIndicator
from invest_bot import InvestBot


def main():
    # Parameters
    HIST_PERIOD = '1y'
    INTERVAL = '1d'
    TICKER = "^GSPC"

    # Downloading financial data
    sp_500_data = yf.download(tickers=TICKER,
                              period=HIST_PERIOD,
                              interval=INTERVAL,
                              auto_adjust=False,
                              multi_level_index=False)

    # Cleaning and formatting data
    sp_500_data = sp_500_data.ffill()
    sp_500_data.dropna(inplace=True)

    # Creating the investment bot
    inv_bot = InvestBot(fin_data=sp_500_data)

    # Applying the strategy
    bb_out_up_signals, fig = inv_bot.bb_out_up_strategy(parameters=None, graph_length=50)

    if bb_out_up_signals['signal'].iloc[-1]:
        msg = f'New signal from bb_out_up strategy:\n'
        msg += f'\t -> {TICKER} value: {round(sp_500_data["Adj Close"].iloc[-1], 2)}'
        inv_bot.send_telegram_alert(msg, fig)


if __name__ == '__main__':
    main()
