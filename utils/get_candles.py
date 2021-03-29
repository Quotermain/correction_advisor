import pandas as pd
from sys import argv

data_path = '/mnt/quik_prices/prices/'

def get_candles(ticker):
    """
    Loads prices from mounted windows folder's csv files
    """
    candles = pd.read_csv(data_path + ticker + '.csv')
    candles['datetime']=pd.to_datetime(candles['datetime'])
    candles.set_index('datetime', inplace=True)
    return candles

if __name__ == '__main__':
    ticker = argv[1]
    print(get_candles(ticker))
