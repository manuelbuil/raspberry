import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
import pdb

start = datetime.datetime(2007, 1, 1)
end = datetime.datetime(2018, 1, 3)
share = web.DataReader('ITX.MC', 'yahoo', start, end)
pdb.set_trace()
share['Adj Close'].plot()
plt.show()
share['Low'].plot()
plt.show()
share['High'].plot()
plt.show()
share['Close'].plot()
plt.show()
