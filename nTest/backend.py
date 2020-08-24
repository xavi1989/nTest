# import stock_info module from yahoo_fin
from yahoo_fin.stock_info import get_data, get_live_price, tickers_sp500
from yahoo_fin import options

#instruction from here:
# http://theautomatic.net/yahoo_fin-documentation/#installation
# http://theautomatic.net/2018/07/31/how-to-get-live-stock-prices-with-python/
# http://theautomatic.net/2019/04/17/how-to-get-options-data-with-python/

class Yahoo_backend:
    def __init__(self, Symbol = None):
        self.symbol = Symbol

    def get_stock_price(self):
        try:
            price = get_live_price(self.symbol)
            return price
        except:
            return 0
        
    def get_expiration_dates(self):
        try:
            return options.get_expiration_dates(self.symbol)
        except:
            print ("Backend error")
            return None

    def get_call_option_at_date(self, Date):
        if Date is None:
            return None

        try:
            return options.get_calls(self.symbol, Date)
        except:
            return None

    def get_put_option_at_date(self, Date):
        if Date is None:
            return None

        try:
            return options.get_puts(self.symbol, Date)
        except:
            return None

    def get_sp500_tickers(self):
        try:
            return tickers_sp500()
        except:
            print ("Backend error")
            return None

if __name__ == '__main__':
    Symbols = ['AAPL', 'GOOG', 'NVDA', 'AMD']

    for sym in Symbols:
        # test price
        bk = Yahoo_backend(sym)
        price = bk.get_stock_price()
        dates = bk.get_expiration_dates()

        if len(dates):
            calls = bk.get_call_option_at_date(dates[0])

            puts = bk.get_put_option_at_date(dates[0])
        
        print("<<<<<<<<<<<<<<<Summary: " + sym)
        print("Stock price = " + str(price))
        print("Option dates:")
        print (dates)
        if len(dates):
            print("Call option:")
            print(calls)
            print("Put option:")
            print(puts)
        print (">>>>>>>>>>>>>>>>>>>>>>End " + sym)
