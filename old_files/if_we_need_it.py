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

'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def logic(account, lookback):
    try:
        today = len(lookback)-1
        if(today > training_period_price): 
            exp_price_moving_average = lookback['close'].ewm(span=training_period_price).mean()[today]  # update PMA
            if(lookback['close'][today] <= exp_price_moving_average):
                if(account.buying_power > 0):
                    account.enter_position('long', account.buying_power, lookback['close'][today])
                    #print("bought at" + str(lookback["date"][today]))
            else:
                if(lookback['close'][today] >= exp_price_moving_average):
                    for position in account.positions:
                            account.close_position(position, 1, lookback['close'][today])
                            #print("sold at" + str(lookback["date"][today]))
    except Exception as e:
        print(e)
    pass 


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
grid_search.to_csv("exp1_no_volume.csv")
print("Done")
print("--- %s seconds ---" % (time.time() - start_time))