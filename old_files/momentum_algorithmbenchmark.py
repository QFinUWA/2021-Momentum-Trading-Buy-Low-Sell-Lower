import pandas as pd
from talib.abstract import *
import time
import sys
import threading


# local imports
from gemini_modules import engine

# read in data preserving dates

# globals
# print("Enter the number of the algorithm to use")
# algorithm_choice = int(input("1: Standard Rolling Average. 2: Moving Average Crossover. 3: Exponential Weighted Moving Average: "))
training_period = int(input("Training period: "))
long_training_period = int(input("Long training period: "))
start_time = time.time()
#print("Loading...")
#backtesting


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


# list_of_coins = ["USDT_ADA", "USDT_BAT", "USDT_BTT", "USDT_DASH", "USDT_ECT","USDT_EOS","USDT_LINK","USDT_NEO","USDT_QTUM","USDT_TRX","USDT_XLM","USDT_XMR","USDT_ZEC"]
#list_of_coins = ["USDT_ADA", "USDT_BAT", "USDT_BTT"]
list_of_coins = ["USDT_ETH"]
print("Running, will take ages")
sys.stdout = open("results1.txt", "w")


def backtest_coin(coiname):
     # for z in range(1,20):
    df = pd.read_csv("new_data/" + coiname + ".csv", parse_dates=[0])
    backtest = engine.backtest(df)
    # print("\n---------------------------------------")
    print("\nCoin: " + coiname)
    backtest.start(100, logic)
    print("Standard Rolling Average")
    backtest.results()
    #backtest.chart()


threads = list()
for x in list_of_coins: #allow choice of number of coins to use
    backtest_coin(x)
    
   
print("Done")
print("--- %s seconds ---" % (time.time() - start_time))
sys.stdout.close()
