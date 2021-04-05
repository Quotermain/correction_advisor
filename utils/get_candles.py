import pickle
import pandas as pd
from sys import argv

def get_candles(ticker):
    """
    Loads raw prices as ndarray of np.void -> translates it to pandas dataframe
    """
    with open(f'/mnt/win_share/prices/{ticker}.pickle', 'rb') as file:
        raw_prices = pickle.load(file)
    df = pd.DataFrame(raw_prices)
    df['time']=pd.to_datetime(df['time'], unit='s')
    df.set_index('time', inplace=True)
    return df

if __name__ == '__main__':
    ticker = argv[1]
    print(get_candles(ticker))
