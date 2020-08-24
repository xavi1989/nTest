from backend import Yahoo_backend

class nStockInterest:
    def __init__(self):
        self.sp500 = Yahoo_backend()

    def get_stock_of_interest(self):
        return self.sp500.get_sp500_tickers()

if __name__ == '__main__':
    sp500 = nStockInterest()
    print (sp500.get_stock_of_interest())