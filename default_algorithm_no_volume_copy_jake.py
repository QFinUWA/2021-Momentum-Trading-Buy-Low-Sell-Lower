import pandas as pd
import pandas_ta as ta
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

def logic_RSI(account, lookback):
    # global price_array
    col_name = "RSI_" + str(training_period_price)
    try:
        today = len(lookback)-1
        volumn_moving_average = lookback['volume'].rolling(window=training_period_price).mean()[today]  # update VMA
        if(lookback[col_name][today] <= 35):
            if(lookback['volume'][today] > volumn_moving_average):
                if(account.buying_power > 0):
                    account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
        elif(lookback[col_name][today] >= 65):
            if(lookback['volume'][today] < volumn_moving_average):
                for position in account.positions:
                    account.close_position(position, 1, lookback['close'][today]*0.9999)
    except Exception as e:
        print(e)
    pass


# grid_search = pd.DataFrame(columns=["Coin","Strategy_Name","Volume_Window","Price_Window","Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold"])
lock = mp.Lock()

list_of_coins = ["USDT_ADA","USDT_BTC","USDT_ETH","USDT_LTC","USDT_XRP"]
# list_of_coins2 = ["USDT_BAT", "USDT_BTT", "USDT_DASH", "USDT_ECT","USDT_EOS","USDT_LINK","USDT_NEO","USDT_QTUM","USDT_TRX","USDT_XLM","USDT_XMR","USDT_ZEC"]

def backtest_coin(coiname,pric,results):
    global training_period_price,lock
    training_period_price = pric
    df = pd.read_csv("data/" + coiname + ".csv", parse_dates=[0])
    # df = pd.read_csv("new_data/" + coiname + ".csv", parse_dates=[0])
    do_rsi = True
    if do_rsi == True:
        col_name = "RSI_" + str(training_period_price)
        df[col_name] = ta.rsi(close=df['close'], length=training_period_price, append=True)
        # print(df.tail())
        backtest = engine.backtest(df)
        backtest.start(1000, logic_RSI)
    else:
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
    for pric in range(5,20):
        # print("PERCENTAGE DONE: "+str(pric*4)+"%")
        # training_period_price = pric
        processes = []
        for i in list_of_coins:
        # for i in list_of_coins2:
            p = mp.Process(target=backtest_coin, args=(i,pric,results))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()
        print(pric)

    df = DataFrame(list(results),columns=["Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold","Coin",'Strategy_Name','Volume_Window','Price_Window'])
    df.to_csv("results.csv",index =False)
    print("Done")
    print('That took {} seconds'.format(time.time() - starttime))
