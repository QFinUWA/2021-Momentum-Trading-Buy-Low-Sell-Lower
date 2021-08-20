import pandas as pd
from talib.abstract import *
import time
import sys
import threading
import numpy as np

# local imports
from gemini_modules import engine



# globals
training_period_price = None
training_period_volume = None
# long_training_period = int(input("Long training period: "))
start_time = time.time()
price_array = np.array([])
volume_array = np.array([])

'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def logic(account, lookback):
    global price_array,volume_array
    try:
        today = len(lookback)-1
        price_array = np.append(price_array,lookback['close'][today])
        volume_array = np.append(volume_array,lookback['volume'][today])

        if(len(price_array) > training_period_price):
            price_array = np.delete(price_array,0)
        
        if(len(volume_array) > training_period_volume):
            volume_array = np.delete(volume_array,0)    
        
        if(today > training_period_price and today > training_period_volume): 
            price_moving_average = np.mean(price_array)
            volume_moving_average = np.mean(volume_array)  
            # print( str(price_moving_average) + " VS" + str(lookback['close'].rolling(window=training_period_price).mean()[today]))
            # print( str(volumn_moving_average) + " VS" + str(lookback['volume'].rolling(window=training_period_price).mean()[today]))
            if(lookback['close'][today] <= price_moving_average):
                if(lookback['volume'][today] >= volume_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today]*1.0001)
            else:
                if(lookback['close'][today] >= price_moving_average):
                    if(lookback['volume'][today] <= volume_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today]*0.9999)

    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset


grid_search = pd.DataFrame(columns=["Coin","Strategy_Name","Volume_Window","Price_Window","Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold"])
# list_of_coins = ["USDT_ADA", "USDT_BAT", "USDT_BTT", "USDT_DASH", "USDT_ECT","USDT_EOS","USDT_LINK","USDT_NEO","USDT_QTUM","USDT_TRX","USDT_XLM","USDT_XMR","USDT_ZEC"]
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
    data['Strategy_Name'] = "Classic"
    data['Volume_Window'] = training_period_volume
    data['Price_Window'] = training_period_price
    grid_search = grid_search.append(data,ignore_index=True)
    lock.release()
    # print("Finished algorithm for coin: "+coiname)


threads = list()

def main():
    global training_period_price,training_period_volume
    for vol in range(1,50):
        training_period_volume = vol
        print("PERCENTAGE DONE: "+str(vol*2)+"%")
        for pric in range(1,50):
            print("PERCENTAGE1 DONE: "+str(pric*2)+"%")
            training_period_price = pric
            for x in list_of_coins:
                try:
                    g = threading.Thread(target=backtest_coin, args=(x,))
                    g.start()
                    threads.append(g)
                    # print("Created thread for: "+x)
                except:
                    print("Error: unable to start thread")
            for index, thread in enumerate(threads):
                thread.join()

print("Running Algorithms...")    
    
main()
   
grid_search.to_csv("results.csv")
print("Done")
print("--- %s seconds ---" % (time.time() - start_time))

