import pandas as pd
from pandas import DataFrame
from talib.abstract import *
import numpy as np

# local imports
from gemini_modules import engine

price_window = 2
price_array = []

#Some how this basic algorithm was optimal..... please read the report before judging us!!!!
def logic(account, lookback):
    global price_window,price_array
    try:
        today = len(lookback)-1
        price_array = np.append(price_array,lookback['close'][today])
        if(len(price_array) > price_window):
            price_array = np.delete(price_array,0) 

        if(today > price_window and len(price_array)>0):
            price_moving_average = np.mean(price_array) 
            if(lookback['close'][today] <= price_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
            else:
                if(lookback['close'][today] >= price_moving_average):
                    for position in account.positions:
                        account.close_position(position, 1, lookback['close'][today]*0.9999)
    except Exception as e:
        print(e)
    pass  


df = pd.read_csv("USDT_LTC.csv" , parse_dates=[0])
backtest = engine.backtest(df)
backtest.start(1000,logic)
backtest.chart()
