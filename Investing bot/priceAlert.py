# -*- coding: utf-8 -*-
"""
Created on April 2021

@author: Julien De Cooman

This code will serve as an alerting tool to detect the best timing to invest in long term position.
"""

import pandas as pd
import yfinance as yf
import sys
import telegram


# simple moving average computation
def sma(prices, period):
    if len(prices) < period:
        print("The dataframe do not contain enough prices to compute the {}-moving average.".format(period))
        sys.exit()
    sma = prices.rolling(window=period).mean()
    return sma


# top Bollinger band computation
def top_bb(prices, sma, period):
    if len(prices) < len(sma) or len(prices) < period:
        print(
            "The dataframe do not contain enough prices to compute the top Bollinger band associated to the {}-moving average.".format(
                period))
        sys.exit()
    moving_std = prices.rolling(window=period).std()
    top_bb = sma + (moving_std * 2)
    return top_bb


# bottom Bollinger band computation
def bottom_bb(prices, sma, period):
    if len(prices) < len(sma) or len(prices) < period:
        print(
            "The dataframe do not contain enough prices to compute the bottom Bollinger band associated to the {}-moving average.".format(
                period))
        sys.exit()
    moving_std = prices.rolling(window=period).std()
    bottom_bb = sma - (moving_std * 2)
    return bottom_bb


# telegram message sending
def send_message_telegram_bot(bot_token, chat_id, msg):
    bot = telegram.Bot(token=bot_token)
    bot.sendMessage(chat_id=chat_id, text=msg)


def main():
    # Telegram parameters
    bot_token = "1655691274:AAHHedeRuokjTZh3o0pGLsT1AZMKL2mr_vg"
    chat_id = 1427772968

    # Prices download
    sp500_df = yf.download('^GSPC', period='1mo', interval='1d')

    # Bollinger band computation
    sp500_df['sma_20'] = sma(prices=sp500_df['Adj Close'], period=20)
    sp500_df['top_bb'] = top_bb(prices=sp500_df['Adj Close'], sma=sp500_df['sma_20'], period=20)
    sp500_df['bottom_bb'] = bottom_bb(prices=sp500_df['Adj Close'], sma=sp500_df['sma_20'], period=20)

    print(sp500_df)

    # -- Alerting -- #
    # Telegram alert if prices cross the sma_20
    if sp500_df['Adj Close'][-1] < sp500_df['sma_20'][-1] and sp500_df['Adj Close'][-2] > sp500_df['sma_20'][-2]:
        msg = "** Ticker: S&P 500 ** \n"
        msg += "Prices crossed downward the 20-day SMA. \n"
        msg += "Price: {} \n".format(round(sp500_df['Adj Close'][-1], 2))
        msg += "SMA_20: {} \n".format(round(sp500_df['sma_20'][-1], 2))
        send_message_telegram_bot(bot_token=bot_token, chat_id=chat_id, msg=msg)

    # Telegram alert if prices cross the bottom Bollinger Band
    if sp500_df['Adj Close'][-1] < sp500_df['bottom_bb'][-1] and sp500_df['Adj Close'][-2] > sp500_df['bottom_bb'][-2]:
        msg = "** Ticker: S&P 500 ** \n"
        msg += "/!\ Price crossed downward the bottom Bollinger Band. \n"
        msg += "Price: {} \n".format(round(sp500_df['Adj Close'][-1], 2))
        msg += "Bottom Bollinger Band: {} \n".format(round(sp500_df['bottom_bb'][-1], 2))
        send_message_telegram_bot(bot_token=bot_token, chat_id=chat_id, msg=msg)

    # Telegram alert if low prices cross the bottom Bollinger Band
    if sp500_df['Low'][-1] < sp500_df['bottom_bb'][-1] and sp500_df['Low'][-2] > sp500_df['bottom_bb'][-2]:
        msg = "** Ticker: S&P 500 ** \n"
        msg += "/!\ Lowest price crossed downward the bottom Bollinger Band. \n"
        msg += "Price: {} \n".format(round(sp500_df['Low'][-1], 2))
        msg += "Bottom Bollinger Band: {} \n".format(round(sp500_df['bottom_bb'][-1], 2))
        send_message_telegram_bot(bot_token=bot_token, chat_id=chat_id, msg=msg)


if __name__ == "__main__":
    main()
