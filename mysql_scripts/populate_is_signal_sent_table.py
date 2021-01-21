from mysql.connector import connect

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
