import pandas as pd
import sys

# classes
from technical_indicator import TechnicalIndicator


class InvestBot:
    def __init__(self, fin_data: pd.DataFrame, parameters: dict):
        self.data = fin_data
        self.parameters = parameters
        print("**New invest bot has been created**")

    def bb_out_up_strategy(self):
        """
        Investment strategy that will identify the first positive closing prices after crossing down the lower Bollinger
        band.
        @return: None
        """

        # Computing the 20-days SMA
        sma_values = TechnicalIndicator.sma(prices=self.data['Adj Close'], days=self.parameters['rolling_days'])
        self.data = self.data.join(sma_values.rename('sma'))

        # Computing the Bollinger bands
        upper_bb, lower_bb = TechnicalIndicator.bollinger_bands(prices=self.data['Adj Close'],
                                                                days=self.parameters['rolling_days'],
                                                                std_factor=self.parameters['std_factor'],
                                                                sma=self.data['sma'])
        self.data = self.data.join(upper_bb).join(lower_bb)

        signal = []
        for i in range(len(self.data)):
            if i == 0:
                signal.append(False)
            elif self.data.iloc[i]['Adj Close'] < self.data.iloc[i]['lower_bb'] \
                    and self.data.iloc[i-1]['Adj Close'] > self.data.iloc[i-1]['lower_bb']:
                signal.append(True)
            else:
                signal.append(False)
        self.data['signal'] = signal

