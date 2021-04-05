
from mysql.connector import connect
import pickle

ALL_TICKERS = [
    'NVTK', 'SBER', 'GAZP', 'POLY', 'TATN', 'LKOH', 'MTSS', 'ROSN', 'MAIL', 'YNDX',
    'PLZL', 'FIVE', 'GMKN', 'MGNT', 'SNGS', 'SNGSP', 'SBERP', 'ALRS', 'MOEX', 'RTKM',
    'VTBR'
]

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
