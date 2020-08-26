# import stock_info module from yahoo_fin
from yahoo_fin.stock_info import get_data, get_live_price, tickers_sp500, get_quote_table
from yahoo_fin import options

from retry.api import retry_call

#instruction from here:
# http://theautomatic.net/yahoo_fin-documentation/#installation
# http://theautomatic.net/2018/07/31/how-to-get-live-stock-prices-with-python/
# http://theautomatic.net/2019/04/17/how-to-get-options-data-with-python/
# http://theautomatic.net/2020/05/05/how-to-download-fundamentals-data-with-python/

Debug = 0

retries = -1

class Yahoo_backend:
    def __init__(self, Symbol = None):
        self.symbol = Symbol
        # set to 0.01 to avoid divided by 0 error
        self.live_price = 0.01
        self.previous_close_price = 0.01

    def get_stock_price(self):
        try:
            self.live_price = retry_call(get_live_price, fargs=[self.symbol], tries = retries)
        except:
            self.live_price = 0
        return self.live_price
    
    def get_previous_close_price(self):
        try:
            table = retry_call(get_quote_table, fargs=[self.symbol, True], tries = retries)
            if Debug:
                print (table)
            self.previous_close_price = table['Previous Close']
        except:
            print ("exception happens in get_previous_close_price")
            self.previous_close_price = 0.01

        return self.previous_close_price

    def get_stock_live_percentage(self):
        return (self.live_price - self.previous_close_price) / self.previous_close_price

    def get_expiration_dates(self):
        try:
            return retry_call(options.get_expiration_dates, fargs=[self.symbol], tries = retries)
        except:
            print ("Backend error")
            return None

    def get_call_option_at_date(self, Date):
        if Date is None:
            return None

        try:
            return retry_call(options.get_calls, fargs=[self.symbol, Date], tries = retries)
        except:
            return None

    def get_put_option_at_date(self, Date):
        if Date is None:
            return None

        try:
            return retry_call(options.get_puts, fargs=[self.symbol, Date], tries = retries)
        except:
            return None

    def get_sp500_tickers(self):
        try:
            return tickers_sp500()
        except:
            print ("Backend error")
            return None

if __name__ == '__main__':
    Symbols = ['AAPL','NVDA', 'AMD']

    for sym in Symbols:
        # test price
        bk = Yahoo_backend(sym)
        price = bk.get_stock_price()
        previous_price = bk.get_previous_close_price()
        percentage = bk.get_stock_live_percentage()
        dates = bk.get_expiration_dates()

        if len(dates):
            calls = bk.get_call_option_at_date(dates[0])

            puts = bk.get_put_option_at_date(dates[0])
        
        print("<<<<<<<<<<<<<<<Summary: " + sym)
        print("Stock price = " + str(price))
        print("previous price = " + str(previous_price))
        print("percentage = " + str(percentage))
        print("Option dates:")
        print (dates)
        if len(dates):
            print("Call option:")
            print(calls)
            print("Put option:")
            print(puts)
        print (">>>>>>>>>>>>>>>>>>>>>>End " + sym)
