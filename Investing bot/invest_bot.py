import pandas as pd
import plotly.graph_objects as go

# classes
from technical_indicator import TechnicalIndicator


class InvestBot:
    def __init__(self, fin_data: pd.DataFrame):
        self.fin_data = fin_data
        print(35 * "_")
        print("**New invest bot has been created**")
        print(35 * "_")

    def bb_out_up_strategy(self, parameters: dict):
        """
        Investment strategy that will identify the first positive closing prices after crossing down the lower Bollinger
        band.
        @param parameters: Bollinger bands parameters.
        @return: financial data with new column 'signals'.
        """

        print("\nBB out-up strategy launched...")

        fin_data = self.fin_data.copy()

        # Computing the 20-days SMA
        sma_values = TechnicalIndicator.sma(prices=fin_data['Adj Close'], days=parameters['rolling_days'])
        fin_data = fin_data.join(sma_values.rename('sma'))

        # Computing the Bollinger bands
        upper_bb, lower_bb = TechnicalIndicator.bollinger_bands(prices=fin_data['Adj Close'],
                                                                days=parameters['rolling_days'],
                                                                std_factor=parameters['std_factor'],
                                                                sma=fin_data['sma'])
        fin_data = fin_data.join(upper_bb).join(lower_bb)

        i = parameters['rolling_days'] + 1
        signals = [False] * i
        while i < len(fin_data):
            if fin_data.iloc[i]['Adj Close'] < fin_data.iloc[i]['lower_bb'] \
                    and fin_data.iloc[i - 1]['Adj Close'] > fin_data.iloc[i - 1]['lower_bb']:
                for j in range(i, len(fin_data)):
                    # if fin_data.iloc[j]['Adj Close'] > fin_data.iloc[j - 1]['Adj Close']:
                    if fin_data.iloc[j]['Adj Close'] > fin_data.iloc[j]['Open']:
                        signals.append(True)
                        i = j + 1
                        break
                    else:
                        signals.append(False)
            else:
                signals.append(False)
                i += 1

        fin_data['signal'] = signals
        print(f"=> {sum(signals)} signal(s) found during the period.")

        return fin_data

    def first_day_month_strategy(self):
        """
        Investment strategy that simply consists of investing the first day of each month.
        @return:
        """

        print("\nFirst day of month strategy launched...")

        fin_data = self.fin_data.copy()

        signals = []
        for i in range(len(fin_data)):
            if fin_data.index[i].day == 1:
                signals.append(True)
            else:
                signals.append(False)

        fin_data['signal'] = signals
        print(f"=> {sum(signals)} signal(s) found during the period.")

        return fin_data

    def back_testing(self, signal_data: pd.DataFrame):
        """
        Method that will evaluate the profitability of a strategy in the past.
        @param signal_data: dataframe containing all data used in the strategy computation as well as signals.
        @return: None
        """

        if 'signal' not in signal_data.columns or signal_data['signal'].empty:
            print("Please compute investing signals before backtesting it.")
            raise ValueError

        position = []
        for i in range(len(signal_data)):
            if signal_data.iloc[i]['signal']:
                position.append(self.fin_data.iloc[i]['Adj Close'])

        buy_value = sum(position)

        sell_value = self.fin_data['Adj Close'].iloc[-1] * len(position)
        ROI = ((sell_value - buy_value) / buy_value) * 100

        print(f"=> The ROI of this investment strategy is {round(ROI, 2)}%.")

    def signal_visualization(self, signal_data: pd.DataFrame):
        """
        Creating graph to visualize investment.
        @param signal_data: dataframe containing all data used in the strategy computation as well as signals.
        @return: None
        """
        fig = go.Figure()

        # Adding the traces
        fig.add_trace(go.Scatter(x=signal_data.index, y=signal_data['Adj Close'], line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=signal_data.index, y=signal_data['upper_bb'], line=dict(color='purple', width=1)))
        fig.add_trace(go.Scatter(x=signal_data.index, y=signal_data['lower_bb'], line=dict(color='purple', width=1)))
        fig.add_trace(go.Scatter(x=signal_data.index, y=signal_data['sma'], line=dict(color='red', width=1)))

        highlighted_signals = signal_data[signal_data['signal']]
        fig.add_trace(go.Scatter(x=highlighted_signals.index, y=highlighted_signals['Adj Close'], mode='markers',
                                 marker=dict(color='green', size=10, symbol='circle')))

        fig.show()
