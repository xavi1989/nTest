from nStock import nStock
from nStockInterest import nStockInterest
from nRules import nRules

import pandas as pd
from datetime import datetime
import os

if __name__ == '__main__':
    pools = nStockInterest().get_self_defined_stocks()
    #sp500 = ['AAPL', 'NVDA']
    df = pd.DataFrame()

    for sym in pools:
        stock = nStock(sym)
        rule = nRules(stock)
        data = rule.process_data_with_rules()
        print (sym)
        print (stock.get_stock_price())
        print (data)

        df = pd.concat([df, data], ignore_index=True)

    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    day = datetime.now().strftime('%d')

    filename = os.getcwd() + '/result/' + year + month + day + '.csv'

    print (filename)
    df.to_csv(filename)

