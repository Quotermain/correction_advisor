from utils.send_message import send_message
from utils.check_signal_is_sent import check_signal_is_sent
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag
from utils.calculate_trade_size import calculate_trade_size

from datetime import datetime
from multiprocessing import Pool
from pandas_datareader import data as pdr
from time import sleep
import pickle
import yfinance as yf
yf.pdr_override()

data_path = './data/thresholds/'

with open(data_path + 'open_close_week_dif_mean.pickle', 'rb') as file:
    open_close_week_dif_mean = pickle.load(file)
with open(data_path + 'open_close_week_dif_std.pickle', 'rb') as file:
    open_close_week_dif_std = pickle.load(file)

with open(data_path + 'open_close_day_dif_mean.pickle', 'rb') as file:
    open_close_day_dif_mean = pickle.load(file)
with open(data_path + 'open_close_day_dif_std.pickle', 'rb') as file:
    open_close_day_dif_std = pickle.load(file)

with open(data_path + 'open_close_hour_dif_mean.pickle', 'rb') as file:
    open_close_hour_dif_mean = pickle.load(file)
with open(data_path + 'open_close_hour_dif_std.pickle', 'rb') as file:
    open_close_hour_dif_std = pickle.load(file)

with open(data_path + 'open_close_5min_dif_mean.pickle', 'rb') as file:
    open_close_5min_dif_mean = pickle.load(file)
with open(data_path + 'open_close_5min_dif_std.pickle', 'rb') as file:
    open_close_5min_dif_std = pickle.load(file)

with open(data_path + 'open_close_1min_dif_mean.pickle', 'rb') as file:
    open_close_1min_dif_mean = pickle.load(file)
with open(data_path + 'open_close_1min_dif_std.pickle', 'rb') as file:
    open_close_1min_dif_std = pickle.load(file)

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

AGG_DICT = {
    'Open': 'first', 'High': 'max', 'Low': 'min',
    'Close': 'last', 'Volume': 'sum'
}


def run(ticker):

    signal_is_sent = check_signal_is_sent(ticker)

    if (not signal_is_sent):

        tf_1min = pdr.get_data_yahoo(ticker, period='1d', interval='1m').loc[
            :, ['Open', 'High', 'Low', 'Close', 'Volume']
        ]
        tf_5min = tf_1min.resample('5Min').agg(AGG_DICT)
        tf_1hour = tf_1min.resample('60Min').agg(AGG_DICT)

        THRESH_5MIN = (
            open_close_5min_dif_mean[ticker] +
            3 * open_close_5min_dif_std[ticker]
        )
        THRESH_1MIN = (
            open_close_1min_dif_mean[ticker] +
            3 * open_close_1min_dif_std[ticker]
        )
        TARGET_THRESH = (
            open_close_5min_dif_mean[ticker] +
            open_close_5min_dif_std[ticker]
        )
        trade_size = calculate_trade_size(
            ticker, TARGET_THRESH, tf_5min.Close[-1]
        )
        condition_short = (
            (
                (tf_5min.Close[-1] - tf_5min.Open[-1]) /
                tf_5min.Open[-1] >= THRESH_5MIN
            ) and
            (
                (tf_1min.Close[-1] - tf_1min.Open[-1]) /
                tf_1min.Open[-1] >= THRESH_1MIN
            )
        )
        condition_long = (
            (
                (tf_5min.Open[-1] - tf_5min.Close[-1]) /
                tf_5min.Open[-1] >= THRESH_5MIN
            ) and
            (
                (tf_1min.Open[-1] - tf_1min.Close[-1]) /
                tf_1min.Open[-1] >= THRESH_1MIN
            )
        )

        cur_time = str(datetime.now().time())
        if condition_short:
            print(cur_time, ticker, ': SHORT')
            messsage = ' '.join([cur_time, ticker, 'SHORT', str(trade_size)])
            send_message(messsage)
            set_signal_is_sent_flag(ticker)
        elif condition_long:
            print(cur_time, ticker, ': LONG')
            messsage = ' '.join([cur_time, ticker, 'LONG', str(trade_size)])
            send_message(messsage)
            set_signal_is_sent_flag(ticker)

if __name__ == '__main__':
    while True:
        with Pool(4) as p:
            p.map(run, ALL_TICKERS)
