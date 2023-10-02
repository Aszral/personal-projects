import datetime as dt
import matplotlib.pyplot as plt
from pandas import data as web

tickers = ['WFC', 'AAPL', 'FB', 'NVDA', 'GS']
amounts = [12, 16, 12, 11, 7]
prices = []
total = []

for ticker in tickers:
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2019, 8, 1), dt.datetime.now())
    price = df[-1:]['Close'][0]
    prices.append(price)
    index = prices.index(price)
    total.append(price * amounts[index])

fig, ax = plt.subplots(figsize=(16, 8))
ax.set_facecolor('black')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

ax.set_title('PORTFOLIO VISUALIZER', color='#EF6C35', fontsize=20)
