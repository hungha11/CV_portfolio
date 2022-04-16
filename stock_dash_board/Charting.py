import vnquant.DataLoader as dl
import pandas as pd
import numpy as np
import datetime
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.lib import resample_apply
from backtesting.test import SMA


def data_for_plotting(symbol):
    start = '2020-01-01'

    # you can fix the time frame by using timedelta function of datetime library
    now = datetime.datetime.now()
    end = now.strftime("%Y-%m-%d")
    loader = dl.DataLoader(symbol, start, end, data_source='VND', minimal=True)
    pricedata = loader.download()

    # format the data for the mplfinance
    stock = pricedata.copy()
    stock.reset_index(inplace=True)

    dailyInfo = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    dailyInfo['Date'] = stock['date']
    dailyInfo['Open'] = stock['open']
    dailyInfo['High'] = stock['high']
    dailyInfo['Low'] = stock['low']
    dailyInfo['Close'] = stock['close']
    dailyInfo['Volume'] = stock['volume']
    dailyInfo.set_index('Date', inplace=True)

    # to store data remove the '#' on the following line
    # csv_file = close_data.to_csv(f'Data/ClosePrice/{symbol} historical since {start}', index=True)

    return dailyInfo

# Bollinger band
def BBupper(array ,n):
    B_MA = pd.Series(array).rolling(n).mean()
    sigma = pd.Series(array).rolling(n).std()

    BU = pd.Series((B_MA + 2 * sigma), name='BU')
    return BU

def BBlower(array ,n):
    B_MA = pd.Series(array).rolling(n).mean()
    sigma = pd.Series(array).rolling(n).std()

    BL = pd.Series((B_MA - 2 * sigma), name='BL')
    return BL


class SmaCross(Strategy):
    n1 = 20
    n2 = 60

    def init(self):
        close = self.data.Close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)
        self.upperband = self.I(BBupper, close, 20)
        self.lowerband = self.I(BBlower, close, 20)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()