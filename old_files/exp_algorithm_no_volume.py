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
            price_moving_average = ema(price_array,training_period_price) 
            
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

def ema(data, window):
    if len(data) < 2 * window:
        raise ValueError("data is too short")
    c = 2.0 / (window + 1)
    current_ema = sma(data[-window*2:-window], window)
    for value in data[-window:]:
        current_ema = (c * value) + ((1 - c) * current_ema)
    return current_ema

def sma( data, window):
    if len(data) < window:
        return None
    return sum(data[-window:]) / float(window)

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
    for pric in range(1,2):
        print("PERCENTAGE DONE: "+str(pric*2)+"%")
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
   
grid_search.to_csv("exp_no_volume.csv")
print("Done")
print("--- %s seconds ---" % (time.time() - start_time))

