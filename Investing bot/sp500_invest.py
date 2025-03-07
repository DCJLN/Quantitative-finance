import pandas as pd
import yfinance as yf
from technical_indicator import TechnicalIndicator
from invest_bot import InvestBot
import asyncio
import telegram


def send_telegram_alert(msg):
    # Parameters
    bot_token = "7191274095:AAHWT5vXJ2owAZXptfxfsXy5hBTsb2AKIMY"
    chat_id = 7162781343
    bot = telegram.Bot(token=bot_token)
    asyncio.run(bot.send_message(chat_id=chat_id, text=msg))


def main():
    # Parameters
    HIST_PERIOD = '3y'
    INTERVAL = '1d'
    TICKER = "^GSPC"

    # Downloading financial data
    sp_500_data = yf.download(tickers=TICKER, period=HIST_PERIOD, interval=INTERVAL, auto_adjust=False,
                              multi_level_index=False)

    # Cleaning and formatting data
    sp_500_data = sp_500_data.ffill()
    sp_500_data.dropna(inplace=True)

    # Creating the investment bot
    inv_bot = InvestBot(fin_data=sp_500_data)

    bb_out_up_signals = inv_bot.bb_out_up_strategy(parameters=None, plotting=False)
    first_d_m_signals = inv_bot.first_day_month_strategy(plotting=False)

    send_telegram_alert(msg='test2')


if __name__ == '__main__':
    main()
