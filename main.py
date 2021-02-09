from utils.send_message import send_message
from utils.check_signal_is_sent import check_signal_is_sent
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag
from utils.calculate_trade_size import calculate_trade_size
from utils.get_candles import get_candles

import pandas as pd
from datetime import datetime
from multiprocessing import Pool
from time import sleep
import pickle
from technical_indicators_lib import RSI

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

with open('data/tickers/ALL_TICKERS.pickle', 'rb') as file:
    ALL_TICKERS = pickle.load(file)

AGG_DICT = {
    'open': 'first', 'high': 'max', 'low': 'min',
    'close': 'last', 'volume': 'sum'
}

def run(ticker):

    #print(ticker)

    signal_is_sent = check_signal_is_sent(ticker)

    if (not signal_is_sent):

        tf_1min = get_candles(ticker, '1m', '7d')
        tf_5min = tf_1min.resample('5Min').agg(AGG_DICT)
        tf_hour = tf_1min.resample('60Min').agg(AGG_DICT)
        tf_day = tf_1min.resample('1D').agg(AGG_DICT)

        rsi = RSI()
        tf_1min = rsi.get_value_df(tf_1min)
        tf_5min = rsi.get_value_df(tf_5min)


        '''THRESH_DAY = (
            open_close_day_dif_mean[ticker]
        )'''
        THRESH_HOUR = (
            open_close_hour_dif_mean[ticker] +
            3 * open_close_hour_dif_std[ticker]
        )
        '''THRESH_5MIN = (
            open_close_5min_dif_mean[ticker] +
            3 * open_close_5min_dif_std[ticker]
        )
        THRESH_1MIN = (
            open_close_1min_dif_mean[ticker] +
            3 * open_close_1min_dif_std[ticker]
        )'''

        condition_short = tf_5min.RSI[-1] >= 70 and tf_1min.RSI[-1] >= 70 and (
            (tf_day.close[-1] - tf_day.open[-1]) /
            tf_day.open[-1] >= 0
        ) and (
            (tf_hour.close[-1] - tf_hour.open[-1]) /
            tf_hour.open[-1] >= THRESH_HOUR
        )
        condition_long = tf_5min.RSI[-1] <= 30 and tf_1min.RSI[-1] <= 30 and (
            (tf_day.open[-1] - tf_day.close[-1]) /
            tf_day.open[-1] >= 0
        ) and (
            (tf_hour.open[-1] - tf_hour.close[-1]) /
            tf_hour.open[-1] >= THRESH_HOUR
        )

        # Trade size depends on STOP_LOSS_THRESH
        STOP_LOSS_THRESH = (
            open_close_5min_dif_mean[ticker] +
            open_close_5min_dif_std[ticker]
        )
        trade_size = calculate_trade_size(
            ticker, STOP_LOSS_THRESH, tf_5min.close[-1]
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
        '''for ticker in ALL_TICKERS:
            run(ticker)'''
        try:
            with Pool(4) as p:
                p.map(run, ALL_TICKERS)
        except KeyboardInterrupt:
            print('Aborting')
        except Exception as e:
            print(e)
            continue
