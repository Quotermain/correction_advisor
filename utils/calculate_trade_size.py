import sys

USDRUB = 75
def calculate_trade_size(ticker, acceptable_PERC_loss, last_close):
    """
    Converts dollars to rubles for proper calculation 
    """
    if '_SPB' in ticker:
        last_close = last_close * USDRUB
    trade_size = 100 / (acceptable_PERC_loss * last_close)
    return trade_size

if __name__ == '__main__':
    acceptable_PERC_loss = float(sys.argv[1])
    last_close = float(sys.argv[2])
    print(calculate_trade_size(acceptable_PERC_loss, last_close))
