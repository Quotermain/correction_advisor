from mysql.connector import connect
import pickle

import os

print(os.listdir('.'))

with open('data/tickers/ALL_TICKERS.pickle', 'rb') as file:
    ALL_TICKERS = pickle.load(file)

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
