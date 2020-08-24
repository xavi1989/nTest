import numpy as np
import pandas as pd
from nStock import nStock

Debug = 0

class nRules:
    '''
    define a set of operations to filter the data from the stock
    '''
    def __init__(self, stock):
        self.stock = stock
        self.stock_price = stock.get_stock_price()
        self.valid = True

        if self.stock_price == 0 or self.stock_price is None:
            self.valid = False
            return

        # default range is from [0.75, 1.25]
        self.strike_price_range_min = 0.75 * self.get_stock_price()
        self.strike_price_range_max = 1.25 * self.get_stock_price()

        # default multiple of base_volume
        self.multiple_of_base_volume = 10

    def set_strike_price_roi(self, min, max):
        self.strike_price_range_min = min * self.get_stock_price()
        self.strike_price_range_max = max * self.get_stock_price()

    def get_stock_price(self):
        return self.stock.get_stock_price()

    def __process_data_with_rules(self, call_or_put):
        # get calls df
        # in case networking not stable and fail to retrieve data
        if call_or_put == 'call':
            df = self.stock.get_next_calls()
        else:
            df = self.stock.get_next_puts()

        if df is None:
            return

        # some data frame pre-processing
        df = df.fillna(0)
        df = df.replace('-', 0)
        df['Volume'] = df['Volume'].astype('int64')

        mean_volume = np.mean(df['Volume'])
        median_volume = np.median(df['Volume'])
        base_volume = np.max([mean_volume, median_volume])
        if Debug:
            print (mean_volume)
            print (median_volume)
            print (base_volume)

        try:
            df['Strike']
        except:
            return None

        index = (df['Strike'] > self.strike_price_range_min) & (df['Strike'] < self.strike_price_range_max) & (df['Volume'] > base_volume * self.multiple_of_base_volume)
        if Debug:
            print (index)
        
        if not any(index):
            if Debug:
                print ("Not found for " +  call_or_put +  " option chain of " + self.stock.get_symbol_name())
                print (df.head())
            maxId = df['Volume'].idxmax()
            index = [False] * df.shape[0]
            index[maxId] = True
            if Debug:
                print (index)
                print (df.shape)
            #return None
        
        # gather potential Strike, 'Last Price', 'Volume'
        ret_df = df.loc[index, ['Strike', 'Last Price', 'Volume']]

        if Debug:
            print (ret_df)
            print (ret_df.ndim)
            print (ret_df.shape)

        if ret_df.ndim == 2:
            length = ret_df.shape[0]
        else:
            length = 1

        ret_df['Symbol'] = [self.stock.get_symbol_name()] * length

        ret_df['Volume_Ratio'] = df['Volume'] / base_volume

        ret_df['Type'] = [call_or_put] * length

        ret_df['Margin'] = (df['Strike'] - self.stock_price) / self.stock_price if call_or_put == 'call' else (self.stock_price - df['Strike']) / self.stock_price

        ret_df['Option_Expiration_Date'] = [self.stock.get_next_expiration_date()] * length

        return ret_df

    def process_data_with_rules(self):
        if self.valid is False:
            return None

        call_ret = self.__process_data_with_rules('call')
        put_ret = self.__process_data_with_rules('put')
        
        if call_ret is None and put_ret is None:
            return None

        ret_df = pd.concat([call_ret, put_ret], ignore_index=True)

        if Debug:
            print (call_ret)
            print (put_ret)
            print (ret_df.head())
        ret_df['Prob'] = ret_df['Last Price'] * ret_df['Volume'] / np.sum(ret_df['Last Price'] * ret_df['Volume'])

        return ret_df
        

if __name__ == '__main__':
    Symbol = 'NVDA'

    stock = nStock(Symbol)
    rules = nRules(stock)

    print (rules.get_stock_price())

    print (rules.process_data_with_rules())





