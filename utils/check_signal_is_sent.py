from mysql.connector import connect
import sys

CRIDENTIALS = {
    'host': 'localhost', 'user': 'root', 'autocommit': True,
    'password': 'Quotermain233', 'database': 'trading'
}

def check_signal_is_sent(ticker):
    query = f'SELECT is_sent FROM is_signal_sent WHERE ticker="{ticker}"'
    connection = connect(**CRIDENTIALS)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()[0]
    return result

if __name__ == '__main__':
    ticker = sys.argv[1]
    print(check_signal_is_sent(ticker))
