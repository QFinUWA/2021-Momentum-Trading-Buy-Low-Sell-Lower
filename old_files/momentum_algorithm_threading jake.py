import pandas as pd
from talib.abstract import *
import time
import sys
import threading

# local imports
from gemini_modules import engine



# globals
algorithm_choice = int(input("1: Standard Rolling Average. 2: Moving Average Crossover. 3: Exponential Weighted Moving Average: "))
training_period = int(input("Training period: "))
if (algorithm_choice == 2):
    long_training_period = int(input("Long training period: "))

start_time = time.time()
grid_search = pd.DataFrame(columns=["Coin","Strategy_Name","Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold"])


'''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''
def logic(account, lookback):
    # print("logic start")
    try:
        today = len(lookback)-1
        if(today > training_period): 
            price_moving_average = lookback['close'].rolling(window=training_period).mean()[today]  # update PMA
            volumn_moving_average = lookback['volume'].rolling(window=training_period).mean()[today]  # update VMA

            if(lookback['close'][today] < price_moving_average):
                if(lookback['volume'][today] > volumn_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today])
                        #print("bought at" + str(lookback["date"][today]))
            else:
                if(lookback['close'][today] > price_moving_average * 1.01):
                    if(lookback['volume'][today] < volumn_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today])
                                # print("sold at" + str(lookback["date"][today]))
        # print("logic end")
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset

def logic2(account, lookback):
    try:
        today = len(lookback)-1
        try:
            yesterday = len(lookback)-2
        except:
            pass
        if(today > training_period): 
            long_price_moving_average = lookback['close'].rolling(window=long_training_period).mean()[today]  # update long average
            short_price_moving_average = lookback['close'].rolling(window=training_period).mean()[today]  # update short average
            yesterday_long_price_moving_average = lookback['close'].rolling(window=long_training_period).mean()[yesterday]  # yesterday long average
            yesterday_short_price_moving_average = lookback['close'].rolling(window=training_period).mean()[yesterday]  # yesterday short average
            volumn_moving_average = lookback['volume'].rolling(window=training_period).mean()[today]  # update VMA

            if(yesterday_short_price_moving_average < yesterday_long_price_moving_average and short_price_moving_average >= long_price_moving_average):
                if(lookback['volume'][today] > volumn_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today])
                        #print("bought at" + str(lookback["date"][today]))
            else:
                if(yesterday_long_price_moving_average < yesterday_short_price_moving_average and long_price_moving_average >= short_price_moving_average):
                    if(lookback['volume'][today] < volumn_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today])
                                #print("sold at" + str(lookback["date"][today]))
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset

def logic3(account, lookback):
    try:
        today = len(lookback)-1
        if(today > training_period): 
            exp_price_moving_average = lookback['close'].ewm(span=training_period).mean()[today]  # update PMA
            volumn_moving_average = lookback['volume'].rolling(window=training_period).mean()[today]  # update VMA

            if(lookback['close'][today] < exp_price_moving_average):
                if(lookback['volume'][today] > volumn_moving_average):
                    if(account.buying_power > 0):
                        account.enter_position('long', account.buying_power, lookback['close'][today])
                        #print("bought at" + str(lookback["date"][today]))
            else:
                if(lookback['close'][today] > exp_price_moving_average):
                    if(lookback['volume'][today] < volumn_moving_average):
                        for position in account.positions:
                                account.close_position(position, 1, lookback['close'][today])
                                #print("sold at" + str(lookback["date"][today]))
    except Exception as e:
        print(e)
    pass  # Handles lookback errors in beginning of dataset



list_of_coins = ["USDT_ADA", "USDT_BAT", "USDT_BTT", "USDT_DASH", "USDT_ECT","USDT_EOS","USDT_LINK","USDT_NEO","USDT_QTUM","USDT_TRX","USDT_XLM","USDT_XMR","USDT_ZEC"]



lock = threading.Lock()

def backtest_coin(coiname):
    global grid_search
    df = pd.read_csv("new_data/" + coiname + ".csv", parse_dates=[0])
    backtest = engine.backtest(df)
    if algorithm_choice == 1:
        backtest.start(100, logic)
        print("Standard Rolling Average")
        stratname = "Standard Rolling Average"
    elif algorithm_choice == 2:
        backtest.start(100, logic2)
        print("Moving Average Crossover")
        stratname = "Moving Average Crossover"
    elif algorithm_choice == 3:
        backtest.start(100, logic3)
        print("Exponential Moving Average")
        stratname = "Exponential Moving Average"

    data = backtest.results()
    data['Coin'] = coiname
    data['Strategy_Name'] = stratname
    lock.acquire()
    grid_search = grid_search.append(data,ignore_index=True)
    lock.release()
    print("Finished algorithm for coin: "+coiname)


threads = list()

for x in list_of_coins:
    try:
        g = threading.Thread(target=backtest_coin, args=(x,))
        g.start()
        threads.append(g)
        print("Created thread for: "+x)
    except:
        print("Error: unable to start thread")

print("Running Algorithms...")    
    
for index, thread in enumerate(threads):
        thread.join()
   
grid_search.to_csv("results.csv")
print("Done")
print("--- %s seconds ---" % (time.time() - start_time))

