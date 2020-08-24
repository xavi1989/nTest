from backend import Yahoo_backend

class nStock:
    '''
        symbol name
        current price
        next_expiration_date
        next_call
        next_put
    '''
    def __init__(self, Symbol):
        self.symbol = Symbol
        self.time = {}
        bk = Yahoo_backend(self.symbol)
        self.current_price = bk.get_stock_price()
        expiration_dates = bk.get_expiration_dates()
        if len(expiration_dates):
            self.next_expiration_date = expiration_dates[0]
            self.next_call = bk.get_call_option_at_date(self.next_expiration_date)
            self.next_put = bk.get_put_option_at_date(self.next_expiration_date)
        else:
            self.next_expiration_date = None
            self.next_call = None
            self.next_put = None

    def get_symbol_name(self):
        return self.symbol

    def get_stock_price(self):
        return self.current_price

    def get_next_expiration_date(self):
        return self.next_expiration_date
    
    def get_next_calls(self):
        return self.next_call
    
    def get_next_puts(self):
        return self.next_put

if __name__ == '__main__':
    Symbol = 'AAPL'

    stock = nStock(Symbol)
    print (stock.get_stock_price())
    print (stock.get_next_expiration_date())
    print (stock.get_next_calls())
    print (stock.get_next_puts())

