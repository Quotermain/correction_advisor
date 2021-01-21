from multiprocessing import Pool
from pandas_datareader import data as pdr
from time import sleep
import yfinance as yf
yf.pdr_override()

ALL_TICKERS = [
    'MTSS.ME', 'AFLT.ME', 'OGKB.ME', 'MGNT.ME', 'TATN.ME', 'MTLR.ME', 'IBM',
    'ALRS.ME', 'SBER.ME', 'MOEX.ME', 'HYDR.ME', 'ROSN.ME', 'LKOH.ME', 'SIBN.ME',
    'GMKN.ME', 'RTKM.ME', 'SNGS.ME', 'CHMF.ME', 'VTBR.ME', 'NVTK.ME', 'GAZP.ME',
    'YNDX.ME', 'NLMK.ME', 'FIVE.ME', 'SBERP.ME', 'SNGSP.ME', 'BTCUSD=X', 'ETHUSD=X',
    'EURUSD=X', 'USDJPY=X', 'GBPUSD=X', 'USDRUB=X', 'AUDUSD=X', 'NZDUSD=X', 'USDHKD=X',
    'USDSGD=X', 'USDMXN=X', 'USDZAR=X', 'USDCNH=X', 'USDCAD=X', 'USDCHF=X', 'AAPL',
    'BA', 'AMZN', 'NVDA', 'FB', 'MSFT', 'MCD', 'TGT', 'V', 'TWTR', 'INTC', 'GOOG',
    'T', 'XOM', 'PFE', 'DIS', 'WMT', 'AMD', 'NFLX', 'MU', 'MA', 'ATVI', 'NKE',
    'CSCO', 'PYPL', 'GE', 'NEM', 'QCOM', 'SBUX', 'ADBE', 'KO', 'KHC', 'CAT', 'BIIB',
    'ABBV', 'EA', 'NEE', 'JNJ', 'CRM', 'UNH', 'FDX', 'BMY', 'CVX', 'HPQ', 'AVGO',
    'DAL', 'PG', 'F', 'GM'
]
AGG_DICT = {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}

def run(ticker):
    tf_1min = pdr.get_data_yahoo(ticker, period='1d', interval='1m').loc[
        :, ['Open', 'High', 'Low', 'Close', 'Volume']
    ]
    tf_5min = tf_1min.resample('5Min').agg(AGG_DICT)
    tf_1hour = tf_1min.resample('60Min').agg(AGG_DICT)
    print(tf_5min)
    sleep(50000)

if __name__ == '__main__':
    while True:
        with Pool(4) as p:
            p.map(run, ALL_TICKERS)
