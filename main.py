from multiprocessing import Pool
from pandas_datareader import data as pdr
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

def run(ticker):
    data = pdr.get_data_yahoo(
        ticker, period='1d', interval='1m'
    )
    print(data)

if __name__ == '__main__':
    while True:
        with Pool(4) as p:
            p.map(run, ALL_TICKERS)
