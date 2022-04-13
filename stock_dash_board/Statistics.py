import pandas as pd
import numpy as np
import datetime
import vnquant.DataLoader as dl
import investpy
import matplotlib.pyplot as plt
import bokeh.plotting as bkp
import plotly.graph_objs as go


class risk_analysis(object):
    def __init__(self, stock_name, index_name, start_date):
        self.stock_name = stock_name
        self.index_name = index_name
        self.start_date = start_date

    def get_data_stock(self, stock_name, start_date):
        start_date = start_date
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        loader = dl.DataLoader(stock_name, start_date, end_date, data_source='VND', minimal=True)
        data = loader.download()
        return data

    def get_index_data(self, index_name, start_date):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%d/%m/%Y')
        end_date = datetime.datetime.today().strftime('%d/%m/%Y')

        index = investpy.get_index_historical_data(index_name, country='vietnam', from_date=start_date,
                                                   to_date=end_date)

        return index

    def data_collection(self):
        # Get index data
        index = self.get_index_data(self.index_name, self.start_date)
        index_data = index.reset_index()
        index_data = index_data.rename(
            columns={'Date': 'date', 'Open': 'open', 'Close': 'close', 'High': 'high', 'Low': 'low',
                     'Volume': 'volume'})
        index_data['date'] = pd.to_datetime(index_data['date'])
        index_data = index_data.set_index('date')
        index_data = index_data.drop('Currency', axis=1)
        index_data['pctchange'] = index_data['close'].pct_change()
        index_data.dropna(inplace=True)

        # Get stock data
        stock = self.get_data_stock(self.stock_name, self.start_date)
        stock_data = stock.reset_index()
        stock_data = stock_data.rename(columns={'Date': 'date', 'Close': 'close'})
        stock_data['date'] = pd.to_datetime(stock_data['date'])
        stock_data = stock_data.set_index('date')
        stock_data = stock_data[['open', 'high', 'low', 'close', 'volume']]
        stock_data['pctchange'] = stock_data['close'].pct_change()
        stock_data.dropna(inplace=True)

        self.index_data = index_data
        self.stock_data = stock_data

        return self.index_data, self.stock_data

    def calculate_std(self):
        index_data, stock_data = self.index_data, self.stock_data

        # Calculate variance
        # var_stock = round(float(['pctchange'].var()),5)
        # Calculate standard deviation
        def variance(data, ddof=0):
            n = len(data)
            mean = sum(data) / n

            return sum((x - mean) ** 2 for x in data) / (n - ddof)

        var_stock = round(variance(stock_data['pctchange']), 5)
        var_stock = var_stock * 100

        stock_variance = 'Variance: ' + str(var_stock).format('.2f') + '%'

        std_stock = round(float(stock_data['pctchange'].std()), 5)
        std_stock = std_stock * 100
        stock_std_deviation = 'Standard deviation: ' + str(std_stock).format('.2f') + '%'

        return std_stock

    def calculate_beta(self):
        index_data, stock_data = self.data_collection()

        # Calculate beta
        def beta(data, data_index):
            return np.cov(data, data_index)[0, 1] / np.var(data_index)

        beta_stock = beta(stock_data['pctchange'], index_data['pctchange'])
        beta_stock = round(beta_stock, 5)

        return beta_stock

    def calculate_alpha(self):
        index_data, stock_data = self.data_collection()

        def beta(data, data_index):
            return np.cov(data, data_index)[0, 1] / np.var(data_index)

        # Calculate alpha
        def alpha(data, data_index):
            return np.mean(data) - beta(data, data_index) * np.mean(data_index)

        alpha_stock = alpha(stock_data['pctchange'], index_data['pctchange'])
        alpha_stock = round(alpha_stock, 5) * 100

        stock_alpha = 'Alpha: ' + str(alpha_stock).format('.2f') + '%'

        return alpha_stock

    def calculate_rsquared(self):
        index_data, stock_data = self.data_collection()

        # Calculate rsquared
        def rsquared(data, data_index):
            return 1 - (np.var(data) / np.var(data_index))

        rsquared_stock = rsquared(stock_data['pctchange'], index_data['pctchange'])
        rsquared_stock = round(rsquared_stock, 5)

        stock_rsquared = 'Rsquared: ' + str(rsquared_stock).format('.2f')

        return rsquared_stock

    def calculate_correlation(self):
        index_data, stock_data = self.data_collection()

        # Calculate correlation
        def correlation(data, data_index):
            return np.corrcoef(data, data_index)[0, 1]

        correlation_stock = correlation(stock_data['pctchange'], index_data['pctchange'])
        correlation_stock = round(correlation_stock, 5)

        stock_correlation = 'Correlation: ' + str(correlation_stock).format('.2f')

        return correlation_stock
