import pandas as pd
from talib.abstract import *
import time

# local imports
from gemini_modules import engine

# read in data preserving dates

# globals
print("Enter the number of the algorithm to use")
algorithm_choice = int(input("1: Standard Rolling Average. 2: Moving Average Crossover. 3: Exponential Weighted Moving Average: "))
training_period = int(input("Training period: "))
if algorithm_choice == 2:
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

# df = pd.read_csv("data/USDT_XRP.csv", parse_dates=[0])
# df2 = pd.read_csv("data/USDT_BTC.csv", parse_dates=[0])
# df3 = pd.read_csv("data/USDT_DOGE.csv", parse_dates=[0])
# df4 = pd.read_csv("data/USDT_ETH.csv", parse_dates=[0])
# df5 = pd.read_csv("data/USDT_LTC.csv", parse_dates=[0])

# list_of_coins = ["USDT_XRP", "USDT_BTC", "USDT_DOGE", "USDT_ETH", "USDT_LTC"]
list_of_coins = ["USDT_LTC"]

for x in list_of_coins: #allow choice of number of coins to use
    print("Loading...")
    df = pd.read_csv("new_data/" + x + ".csv", parse_dates=[0])
    print("Backtesting...")
    backtest = engine.backtest(df)
    if __name__ == "__main__":
        if algorithm_choice == 1:
            backtest.start(100, logic)
            print("Backtesting complete")
        elif algorithm_choice == 2:
            backtest.start(100, logic2)
            print("Backtesting complete")
        elif algorithm_choice == 3:
            backtest.start(100, logic3)
            print("Backtesting complete")
        print("\nCoin: " + x)
        backtest.results()
        print("short training period = " + str(training_period))
        try:
            print("long training period = " + str(long_training_period))
        except:
            pass
        backtest.chart(x) #add all the coins to the one page
print("Done")
print("--- %s seconds ---" % (time.time() - start_time))

