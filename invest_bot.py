import pandas as pd

# classes
from technical_indicator import TechnicalIndicator


class InvestBot:
    def __init__(self, fin_data: pd.DataFrame):
        self.data = fin_data
        print(35 * "_")
        print("**New invest bot has been created**")
        print(35 * "_")
        print("")

    def bb_out_up_strategy(self, parameters: dict):
        """
        Investment strategy that will identify the first positive closing prices after crossing down the lower Bollinger
        band.
        @return: None
        """

        print("BB out-up strategy launched...")

        # Computing the 20-days SMA
        sma_values = TechnicalIndicator.sma(prices=self.data['Adj Close'], days=parameters['rolling_days'])
        self.data = self.data.join(sma_values.rename('sma'))

        # Computing the Bollinger bands
        upper_bb, lower_bb = TechnicalIndicator.bollinger_bands(prices=self.data['Adj Close'],
                                                                days=parameters['rolling_days'],
                                                                std_factor=parameters['std_factor'],
                                                                sma=self.data['sma'])
        self.data = self.data.join(upper_bb).join(lower_bb)

        signal = []
        i = 0
        while i < len(self.data):
            if i == 0:
                signal.append(False)
                i += 1
            elif self.data.iloc[i]['Adj Close'] < self.data.iloc[i]['lower_bb'] \
                    and self.data.iloc[i-1]['Adj Close'] > self.data.iloc[i-1]['lower_bb']:
                for j in range(i, len(self.data)):
                    if self.data.iloc[j]['Adj Close'] > self.data.iloc[j-1]['Adj Close']:
                        signal.append(True)
                        i = j + 1
                        break
                    else:
                        signal.append(False)
            else:
                signal.append(False)
                i += 1
        self.data['signal'] = signal
        print(f"=> {sum(self.data['signal'])} signal(s) found during the period.")

    @staticmethod
    def back_testing():
        print("To do")
