import sys
import pandas as pd


class TechnicalIndicator:
    @staticmethod
    def sma(prices: pd.DataFrame, days: int):
        """
        Computes the simple moving average.
        @param prices: historical prices data
        @param days: number of rolling days
        @return: DataFrame containing the SMA values
        """
        if len(prices) < days:
            print(f"The df does not contain enough prices to compute the {days}-sma.")
            sys.exit()
        sma = prices.rolling(window=days).mean()
        return sma

    @staticmethod
    def bollinger_bands(prices: pd.DataFrame, days: int, std_factor: int, sma: pd.DataFrame):
        """
        Compute the upper and lower Bollinger bands
        @param prices: historical prices data
        @param days: number of rolling days
        @param std_factor: multiplication factor of std
        @param sma: SMA data needed for the bands computation
        @return: DataFrame containing lower and upper bands data
        """
        if len(prices) < len(sma) or len(prices) < days:
            print(f"The df does not contain enough prices or sma values to compute the Bollinger bands.")
            sys.exit()
        rstd = prices.rolling(window=days).std()
        upper_band = sma + (rstd * std_factor)
        upper_band = upper_band.rename('upper_bb')
        lower_band = sma - (rstd * std_factor)
        lower_band = lower_band.rename('lower_bb')

        return upper_band, lower_band
