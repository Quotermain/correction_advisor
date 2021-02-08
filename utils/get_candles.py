import pandas as pd
from sys import argv
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
pd.options.mode.chained_assignment = None

COL_NAMES = {
    'Open': 'open', 'High': 'high', 'Low': 'low',
    'Close': 'close', 'Volume': 'volume'
}

def get_candles(ticker, interval, period):
    df = pdr.get_data_yahoo(
        ticker, period=period, interval=interval, progress=False
    ).loc[:, ['Open', 'High', 'Low', 'Close', 'Volume']]
    df.rename(columns=COL_NAMES, inplace=True)
    return df

if __name__ == '__main__':
    ticker, interval, period = argv[1], argv[2], argv[3]
    print(get_candles(ticker, interval, period))
