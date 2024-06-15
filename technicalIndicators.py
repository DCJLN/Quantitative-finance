import sys

# simple moving average
def sma(prices, period):
    if len(prices) < period:
        print("The dataframe do not contain enough prices to compute the {}-moving average.".format(period))
        sys.exit()
    sma = prices.rolling(window=period).mean()
    return sma
    

# top Bollinger band
def top_bb(prices, sma, period):
    if len(prices) < len(sma) or len(prices) < period:
        print("The dataframe do not contain enough prices to compute the top Bollinger band associated to the {}-moving average.".format(period))
        sys.exit()
    moving_std = prices.rolling(window=period).std()
    top_bb = sma + (moving_std * 2)
    return top_bb


# bottom Bollinger band
def bottom_bb(prices, sma, period):
    if len(prices) < len(sma) or len(prices) < period:
        print("The dataframe do not contain enough prices to compute the bottom Bollinger band associated to the {}-moving average.".format(period))
        sys.exit()
    moving_std = prices.rolling(window=period).std()
    bottom_bb = sma - (moving_std * 2)
    return bottom_bb