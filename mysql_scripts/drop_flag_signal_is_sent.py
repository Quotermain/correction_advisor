from mysql.connector import connect
import sys
import pickle

CRIDENTIALS = {
    'host': 'localhost', 'user': 'root',
    'password': 'Quotermain233', 'database': 'trading'
}
connection = connect(**CRIDENTIALS)

def drop_flag_signal_is_sent(ticker):
    if ticker == 'ALL':
        query = f'UPDATE is_signal_sent SET is_sent = 0 WHERE is_sent = 1'
    else:
        query = f'UPDATE is_signal_sent SET is_sent = 0 WHERE ticker = "{ticker}"'
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

if __name__ == '__main__':
    ticker = sys.argv[1]
    drop_flag_signal_is_sent(ticker)
