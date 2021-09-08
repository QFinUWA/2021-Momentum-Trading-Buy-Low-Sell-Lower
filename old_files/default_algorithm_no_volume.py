import pandas as pd
from talib.abstract import *
import time
import threading
import numpy as np

# local imports
from gemini_modules import engine

# globals
training_period_price = None
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
            # print( str(price_moving_average) + " VS" + str(lookback['close'].rolling(window=training_period_price).mean()[today]))
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
lock = threading.Lock()

list_of_coins = ["USDT_ADA","USDT_BTC","USDT_ETH","USDT_LTC","USDT_XRP"]

def backtest_coin(coiname):
    global grid_search
    df = pd.read_csv("data/" + coiname + ".csv", parse_dates=[0])
    backtest = engine.backtest(df)
    backtest.start(100000, logic)
    lock.acquire()
    data = backtest.results()
    data['Coin'] = coiname
    data['Strategy_Name'] = "Classic_No_Volume"
    data['Volume_Window'] = "None"
    data['Price_Window'] = training_period_price
    grid_search = grid_search.append(data,ignore_index=True)
    lock.release()

threads = list()

def main():
    global training_period_price
    for pric in range(10,11):
        print("PERCENTAGE DONE: "+str(pric*4)+"%")
        print(pric)
        training_period_price = pric
        for x in list_of_coins:
            try:
                # g = threading.Thread(target=backtest_coin, args=(x,))
                # g.start()
                # threads.append(g)
                backtest_coin(x)
            except:
                print("Error: unable to start thread")
        for thread in threads:
            thread.join()

 
if __name__ == "__main__":
    print("Running Algorithms...")   
    main()
    grid_search.to_csv("default_no_volume.csv")
    print(grid_search.head())
    print("Done")
    print("--- %s seconds ---" % (time.time() - start_time))

