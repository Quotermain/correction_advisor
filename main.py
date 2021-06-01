
from utils.calculate_trade_size import calculate_trade_size
from utils.check_signal_is_sent import check_signal_is_sent
from utils.get_candles import get_candles
from utils.load_pickle_object import load_pickle_object
from utils.send_message import send_message
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag

from datetime import datetime
from multiprocessing import Pool
import pandas as pd
import pickle
from os import listdir
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator
from time import sleep
pd.options.mode.chained_assignment = None  # default='warn'

data_path = './data/thresholds/'
ticker_info = load_pickle_object('data/ticker_info.pickle')
open_close_hour_dif_mean = load_pickle_object(data_path + 'open_close_hour_dif_mean.pickle')
open_close_hour_dif_std = load_pickle_object(data_path + 'open_close_hour_dif_std.pickle')

prices_path = '/mnt/win_share/prices/'
ALL_TICKERS = [file_name.split('.')[0] for file_name in listdir(prices_path)]

AGG_DICT = {
    'open': 'first', 'high': 'max', 'low': 'min',
    'close': 'last', 'real_volume': 'sum'
}

def run(ticker):

    signal_is_sent = check_signal_is_sent(ticker)

    if (not signal_is_sent):

        tf_1hour = get_candles(ticker)
        rsi_1hour = RSIIndicator(close=tf_1hour.close).rsi()
        bolinger_1hour = BollingerBands(close=tf_1hour.close)

        condition_short = rsi_1min[-1] >= 80 and rsi_5min[-1] >= 80
        condition_long = rsi_1min[-1] <= 20 and rsi_5min[-1] <= 20

        # Trade size depends on STOP_LOSS_THRESH. MT5 limitations.
        STOP_LOSS_THRESH = (
            open_close_hour_dif_mean[ticker]
        )
        trade_size = calculate_trade_size(
            STOP_LOSS_THRESH, tf_1min.close[-1]
        ) / ticker_info[ticker]['min_lot']
        trade_size = round(trade_size)

        cur_time = str(datetime.now().time())
        if condition_short:
            sl = round(
                tf_1min.close[-1] + STOP_LOSS_THRESH * tf_1min.close[-1],
                ticker_info[ticker]['price_digits']
            )
            tp = round(
                tf_1min.close[-1] - STOP_LOSS_THRESH * tf_1min.close[-1],
                ticker_info[ticker]['price_digits']
            )
            print('\n', cur_time, ticker, ': SHORT', str(trade_size), tf_1min.close[-1], sl, tp, '\n')
            messsage = ' '.join(
                [cur_time, ticker, 'SHORT', str(trade_size), str(sl), str(tp)]
            )
            send_message(messsage)
            set_signal_is_sent_flag(ticker)
        elif condition_long:
            sl = round(
                tf_1min.close[-1] - STOP_LOSS_THRESH * tf_1min.close[-1],
                ticker_info[ticker]['price_digits']
            )
            tp = round(
                tf_1min.close[-1] + STOP_LOSS_THRESH * tf_1min.close[-1],
                ticker_info[ticker]['price_digits']
            )
            print('\n', cur_time, ticker, ': LONG', str(trade_size), tf_1min.close[-1], sl, tp, '\n')
            messsage = ' '.join(
                [cur_time, ticker, 'LONG', str(trade_size), str(sl), str(tp)]
            )
            send_message(messsage)
            set_signal_is_sent_flag(ticker)

if __name__ == '__main__':
    '''while True:
        try:
            with Pool(4) as p:
                p.map(run, ALL_TICKERS)
        except KeyboardInterrupt:
            print('Aborting')
        except (EOFError, KeyError, pickle.UnpicklingError, ValueError):
            continue
        except Exception as e:
            try:
                print(e)
                continue
            except Exception:
                print('Can"t print')
                continue'''

    while True:
        for ticker in ALL_TICKERS:
            run(ticker)
