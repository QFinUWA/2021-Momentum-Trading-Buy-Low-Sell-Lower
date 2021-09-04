import pandas as pd
from pandas import DataFrame
from talib.abstract import *
import time
import numpy as np
import multiprocessing as mp

# local imports
from gemini_modules import engine

# globals
# training_period_price = 0
start_time = time.time()
price_array = np.array([])


'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def logic(account, lookback):
    global price_array
    try:
        today = len(lookback)-1
        price_array = np.append(price_array,lookback['close'][today])
        if(len(price_array) > training_period_price):
            price_array = np.delete(price_array,0) 
        if(today > training_period_price): 
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
    pass  # Handles lookback errors in beginning of dataset


grid_search = pd.DataFrame(columns=["Coin","Strategy_Name","Volume_Window","Price_Window","Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold"])
lock = mp.Lock()

list_of_coins = ["USDT_ADA","USDT_BTC","USDT_ETH","USDT_LTC","USDT_XRP"]

def backtest_coin(coiname,pric,results):
    global training_period_price,lock
    training_period_price = pric
    df = pd.read_csv("data/" + coiname + ".csv", parse_dates=[0])
    backtest = engine.backtest(df)
    backtest.start(1000, logic)
    lock.acquire()
    data = backtest.results()
    data.append(coiname) #coinname
    data.append("Classic_No_Volume")#'Strategy_Name'
    data.append("None")#'Volume_Window'
    data.append(training_period_price)#'Price_Window'
    results.append(data)
    lock.release()

if __name__ == "__main__":
    print("Running Algorithms...")
    # print(training_period_price)
    # global training_period_price
    # training_period_price = 5
    # print("--- %s seconds ---" % (time.time() - start_time))
    manager = mp.Manager()
    results = manager.list()
    starttime = time.time()
    for pric in range(8,10):
        # print("PERCENTAGE DONE: "+str(pric*4)+"%")
        # training_period_price = pric
        # print(training_period_price)
        processes = []
        for i in list_of_coins:
            p = mp.Process(target=backtest_coin, args=(i,pric,results))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()

    df = DataFrame(list(results),columns=["Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold","Coin",'Strategy_Name','Volume_Window','Price_Window'])
    df.to_csv("results.csv",index =False)
    print("Done")
    print('That took {} seconds'.format(time.time() - starttime))
