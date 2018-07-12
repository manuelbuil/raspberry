import datetime

import matplotlib.pyplot as plt
import pandas_datareader.data as web

def plot(data):
#start = datetime.datetime(2013, 3, 1)
#end = datetime.datetime(2013, 8, 1)
#share = web.DataReader('SAN.MC', 'yahoo', start, end)
    data['Adj Close'].plot()
    plt.title("Adj Close")
    plt.show()
    data['Low'].plot()
    plt.title("Low")
    plt.show()
    data['High'].plot()
    plt.title("High")
    plt.show()
    data['Close'].plot()
    plt.title("Close")
    plt.show()
