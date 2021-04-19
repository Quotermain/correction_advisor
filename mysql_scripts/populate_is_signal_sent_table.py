from mysql.connector import connect
import pickle
from os import listdir

prices_path = '/mnt/win_share/prices/'
ALL_TICKERS = [file_name.split('.')[0] for file_name in listdir(prices_path)]

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
