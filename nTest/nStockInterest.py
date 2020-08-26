from backend import Yahoo_backend

class nStockInterest:
    def __init__(self):
        self.sp500 = Yahoo_backend()

    def get_stock_of_interest(self):
        return self.sp500.get_sp500_tickers()

    def get_self_defined_stocks(self):
        self_list = ['AAPL','ABT','AMZN','AMC','AMD','ATVI','AVGO','BA','BABA','BILI','BP','CAR','CCL','COST','CSCO','DELL','DIS','DOCU','ENS','EOG','FB','FL','GE','GILD','GME','GOOG','HTZ','INO','INTC','JD','JWN','KC','LMT','M','MRK','MRNA','MSFT','NFLX','NIO','NKE','NKLA','NTES','NVAX','NVDA','ORCL','PDD','PFE','PXLW','RCL','RTX','SBUX','SNAP','SPOT','TEAM','TME','TSLA','TSM','TWTR','UAL','UBER','WB','WORK','XLNX','ZM','ZNGA','HAS','SPG','CAKE','DOW','SBUX','RCL','IRBT','XLNX','GME','TTWO','NOK']
        return self_list

if __name__ == '__main__':
    pool = nStockInterest()
    print (pool.get_stock_of_interest())

    self_list = pool.get_self_defined_stocks()

    print (self_list)