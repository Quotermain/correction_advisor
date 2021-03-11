
from utils.calculate_trade_size import calculate_trade_size
from utils.check_signal_is_sent import check_signal_is_sent
from utils.get_candles import get_candles
from utils.load_pickle_object import load_pickle_object
from utils.send_message import send_message
from utils.set_signal_is_sent_flag import set_signal_is_sent_flag

from datetime import datetime
from multiprocessing import Pool
import pandas as pd
from technical_indicators_lib import RSI
from time import sleep
pd.options.mode.chained_assignment = None  # default='warn'

data_path = './data/thresholds/'
open_close_hour_dif_mean = load_pickle_object(data_path + 'open_close_hour_dif_mean.pickle')
open_close_hour_dif_std = load_pickle_object(data_path + 'open_close_hour_dif_std.pickle')
ALL_TICKERS = open_close_hour_dif_mean.keys()
AGG_DICT = {
    'open': 'first', 'high': 'max', 'low': 'min',
    'close': 'last', 'real_volume': 'sum'
}

def run(ticker):

    signal_is_sent = check_signal_is_sent(ticker)

    if (not signal_is_sent):

        tf_1min = get_candles(ticker)
        tf_hour = tf_1min.resample('60Min').agg(AGG_DICT)

        rsi = RSI()
        rsi.get_value_df(tf_1min)

        # If size of a bar exceeds this threshold then try to open position
        THRESH_HOUR = (
            open_close_hour_dif_mean[ticker]
            + 3 * open_close_hour_dif_std[ticker]
        )

        condition_short = tf_1min.RSI[-1] >= 70 and (
            (tf_hour.close[-1] - tf_hour.open[-1]) /
            tf_hour.open[-1] >= THRESH_HOUR
        )
        condition_long = tf_1min.RSI[-1] <= 30 and (
            (tf_hour.open[-1] - tf_hour.close[-1]) /
            tf_hour.open[-1] >= THRESH_HOUR
        )

        # Trade size depends on STOP_LOSS_THRESH
        STOP_LOSS_THRESH = (
            open_close_hour_dif_mean[ticker]
        )
        trade_size = calculate_trade_size(
            STOP_LOSS_THRESH, tf_1min.close[-1]
        )

        cur_time = str(datetime.now().time())
        if condition_short:
            sl = tf_1min.close[-1] + STOP_LOSS_THRESH * tf_1min.close[-1]
            tp = tf_1min.close[-1] - STOP_LOSS_THRESH * tf_1min.close[-1]
            print('\n', cur_time, ticker, ': SHORT', str(trade_size), sl, tp, '\n')
            messsage = ' '.join(
                [cur_time, ticker, 'SHORT', str(trade_size), str(sl), str(tp)]
            )
            send_message(messsage)
            set_signal_is_sent_flag(ticker)
        elif condition_long:
            sl = tf_1min.close[-1] - STOP_LOSS_THRESH * tf_1min.close[-1]
            tp = tf_1min.close[-1] + STOP_LOSS_THRESH * tf_1min.close[-1]
            print('\n', cur_time, ticker, ': LONG', str(trade_size), sl, tp, '\n')
            messsage = ' '.join(
                [cur_time, ticker, 'LONG', str(trade_size), str(sl), str(tp)]
            )
            send_message(messsage)
            set_signal_is_sent_flag(ticker)

if __name__ == '__main__':
    while True:
        try:
            with Pool(4) as p:
                p.map(run, ALL_TICKERS)
        except KeyboardInterrupt:
            print('Aborting')
        except Exception as e:
            try:
                print(e)
                continue
            except Exception:
                print('Can"t print')
                continue
