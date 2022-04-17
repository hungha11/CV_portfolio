from stock_dash_board.quantData import Dataloading as dm
import datetime

start = '2020-01-01'
# you can fix the time frame by using timedelta function of datetime library
now = datetime.datetime.now()
end = now.strftime("%Y-%m-%d")
loader = dm.DataLoader('HAH', start, end, data_source='VND', minimal=True)
data = loader.download()
close_data = data['close'].dropna()
data.reset_index()
print(data)