import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
import plotly.graph_objects as go
import yfinance as yf


# Technical indicator functions
def sma(df: pd.DataFrame, days: int):
    """
    Computes the Simple Moving Average
    :param df: historical data
    :param days: number of rolling days
    :return: DataFrame containing the SMA data
    """
    return df.rolling(days).mean()


def bollinger_bands(df: pd.DataFrame, days: int, std_factor: int, sma: pd.DataFrame):
    """
    Computes the upper and lower Bollinger bands
    :param df:  historical data
    :param days: number of rolling days
    :param std_factor: multiplication factor of std
    :param sma: the sma data used for the bands computations
    :return: Dataframe containing upper and lower bands data
    """
    rstd = df.rolling(days).std()
    upper_band = sma + (std_factor * rstd)
    lower_band = sma - (std_factor * rstd)
    return upper_band, lower_band

def plot_bollinger_bands(df: pd.DataFrame, invest_opp: bool):
    """
    Computes the upper and lower Bollinger bands
    :param df:  Computed SMA and Bollinger data
    :return: figure
    """
    sns.set_style("darkgrid")
    fig = plt.figure(figsize=(10, 6), dpi=200)
    sns.lineplot(data=data, x='Date', y='Adj Close')
    sns.lineplot(data=data, x='Date', y=f'Adj Close_sma{ROLLING_DAYS}', color='red')
    sns.lineplot(data=data, x='Date', y=f'Adj Close_lower_band_{STD_FACTOR}std', color='orange', linestyle='--')
    sns.lineplot(data=data, x='Date', y=f'Adj Close_upper_band_{STD_FACTOR}std', color='orange', linestyle='--')
    plt.fill_between(x=data.index, y1=data[f'Adj Close_lower_band_{STD_FACTOR}std'], y2=data[f'Adj Close_upper_band_{STD_FACTOR}std'], color='orange', alpha=0.1)
    if invest_opp:
        sns.scatterplot(data=data, x='Date', y='Invest', color='purple')
    plt.title('S&P 500 Adj Closing Prices')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
    
def check_invest_opp(df: pd.DataFrame):
    """
    """
    if (df['Adj Close'] <= df[f'Adj Close_sma{ROLLING_DAYS}'] and df['Adj Close_-1'] > df[f'Adj Close_sma{ROLLING_DAYS}'])\
    or (df['Adj Close'] <= df[f'Adj Close_lower_band_{STD_FACTOR}std'] and df['Adj Close_-1'] > df[f'Adj Close_lower_band_{STD_FACTOR}std']):
        return df['Adj Close']
    else:
        return None
    

# Parameters
ROLLING_DAYS = 20
STD_FACTOR = 2
HIST_PERIOD = '1y'
INTERVAL = '1d'

# Downloading portfolio data
ticker = "^GSPC"
data = yf.download(tickers=ticker, period=HIST_PERIOD, interval=INTERVAL)

# Cleaning and formatting data
data = data.fillna(method='ffill')
data.dropna(inplace=True)
data['Adj Close_-1'] = data['Adj Close'].shift(1)

# Computing the 20-days SMA
sma = sma(df=data['Adj Close'], days=ROLLING_DAYS)
data = data.join(sma, rsuffix=f'_sma{ROLLING_DAYS}')

# Computing the Bollinger bands
upper_bb, lower_bb = bollinger_bands(df=data['Adj Close'], days=ROLLING_DAYS, std_factor=STD_FACTOR, sma=sma)
data = data.join(upper_bb, rsuffix=f'_upper_band_{STD_FACTOR}std').join(lower_bb, rsuffix=f'_lower_band_{STD_FACTOR}std')

# checking date of investment
data['Invest'] = data.apply(check_invest_opp, axis=1)

# displaying data
plot_bollinger_bands(df=data, invest_opp=True)

