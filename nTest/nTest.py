from nStock import nStock
from nStockInterest import nStockInterest
from nRules import nRules

if __name__ == '__main__':
    sp500 = nStockInterest().get_stock_of_interest()
    #sp500 = ['AAPL', 'NVDA']
    for sym in sp500:
        stock = nStock(sym)
        rule = nRules(stock)
        data = rule.process_data_with_rules()
        print (sym)
        print (stock.get_stock_price())
        print (data)

