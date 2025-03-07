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

    def bb_out_up_strategy(self, plotting: bool, parameters=None):
        """
        Investment strategy that will identify the first positive closing prices after crossing down the lower Bollinger
        band.
        @param parameters: Bollinger bands parameters.
        @param plotting: determine if graph for visualization has to be created.
        @return: financial data with new column 'signals'.
        """

        if parameters is None:
            parameters = {'rolling_days': 20, 'std_factor': 2}

        print("\nBB out-up strategy launched...")

        fin_data = self.fin_data.copy()

        # Computing the 20-days SMA
        sma_values = TechnicalIndicator.sma(prices=fin_data['Adj Close'], days=parameters['rolling_days'])
        fin_data = fin_data.join(sma_values.rename(f'sma_{parameters["rolling_days"]}'))

        # Computing the Bollinger bands
        upper_bb, lower_bb = TechnicalIndicator.bollinger_bands(prices=fin_data['Adj Close'],
                                                                days=parameters['rolling_days'],
                                                                std_factor=parameters['std_factor'],
                                                                sma=fin_data[f'sma_{parameters["rolling_days"]}'])
        fin_data = fin_data.join(upper_bb).join(lower_bb)

        i = parameters['rolling_days'] + 1
        signals = [False] * i
        while i < len(fin_data):
            if (fin_data.iloc[i]['Adj Close'] < fin_data.iloc[i]['lower_bb']
                    and fin_data.iloc[i - 1]['Adj Close'] > fin_data.iloc[i - 1]['lower_bb']):
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

        if plotting:
            fig = go.Figure(layout=dict(template="plotly_dark"))
            fig.add_trace(go.Scatter(x=fin_data.index, y=fin_data['Adj Close']))
            fig.add_trace(go.Scatter(x=fin_data.index, y=fin_data['upper_bb'], fill=None,
                                     line=dict(color='rgba(128, 0, 128, 0.1)', width=1)))
            fig.add_trace(go.Scatter(x=fin_data.index, y=fin_data['lower_bb'], fill='tonexty',
                                     line=dict(color='rgba(128, 0, 128, 0.1)', width=1), fillcolor='rgba(178, 102, 255, 0.15)'))
            fig.add_trace(go.Scatter(x=fin_data.index, y=fin_data[f'sma_{parameters["rolling_days"]}'], line=dict(color='red', width=1)))

            highlighted_signals = fin_data[fin_data['signal']]
            fig.add_trace(go.Scatter(x=highlighted_signals.index, y=highlighted_signals['Adj Close'], mode='markers',
                                     marker=dict(color='yellow', size=8, symbol='circle')))
            fig.update_layout(showlegend=False)
            fig.show()

        return fin_data

    def first_day_month_strategy(self, plotting: bool):
        """
        Investment strategy that simply consists of investing the first day of each month.
        @param plotting: determine if graph for visualization has to be created.
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

        if plotting:
            fig = go.Figure(layout=dict(template="plotly_dark"))

            fig.add_trace(go.Scatter(x=fin_data.index, y=fin_data['Adj Close']))

            highlighted_signals = fin_data[fin_data['signal']]
            fig.add_trace(go.Scatter(x=highlighted_signals.index, y=highlighted_signals['Adj Close'], mode='markers',
                                     marker=dict(color='yellow', size=10, symbol='circle')))
            fig.update_layout(showlegend=False)
            fig.show()

        return fin_data
