import vnquant.DataLoader as dl
import pandas as pd
import numpy as np
import datetime
import investpy


def load_stock_data(symbol):
    start = '2020-01-01'
    # you can fix the time frame by using timedelta function of datetime library
    now = datetime.datetime.now()
    end = now.strftime("%Y-%m-%d")
    loader = dl.DataLoader(symbol, start, end, data_source='VND', minimal=True)
    data = loader.download()
    close_data = data['close'].dropna()
    data.reset_index()

    return data

    # index data
def load_index_data(index='VN'):
    start = '2020-01-01'
    index = index
    end = datetime.datetime.now()
    index = investpy.get_index_historical_data(x, country='vietnam', from_date='01/01/2019',
                                                   to_date=end.strftime('%d/%m/%Y'))
    index = pd.DataFrame(index)
    index = index.drop(columns=['Currency'])
    index = index.reset_index()
    return index


if __name__ =='__main__':

    x = load_stock_data('MSN')
    print(x)
