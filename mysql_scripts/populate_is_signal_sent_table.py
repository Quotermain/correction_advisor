
from mysql.connector import connect
import pickle

data_path = './data/thresholds/'
with open(data_path + 'open_close_hour_dif_std.pickle', 'rb') as file:
    ALL_TICKERS = pickle.load(file).keys()

CRIDENTIALS = {
    'host': 'localhost', 'user': 'root', 'autocommit': True,
    'password': 'Quotermain233', 'database': 'trading'
}
connection = connect(**CRIDENTIALS)

for ticker in ALL_TICKERS:
    query = f'INSERT INTO is_signal_sent (ticker, is_sent) VALUES ("{ticker}", 0)'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()
