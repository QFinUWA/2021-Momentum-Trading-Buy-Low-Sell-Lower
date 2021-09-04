import pandas as pd

df = pd.read_csv("data/USDT_BTC.csv")

#Question 1
print(df["close"])

#Question 2
print(df.loc[19])


# from talib.abstract import *

# # local imports
# from gemini_modules import engine

# # read in data preserving dates
# df = pd.read_csv("data/USDT_BTC.csv", parse_dates=[0])

# # globals
# training_period = 10
# long_training_period = 20
# #backtesting
# backtest = engine.backtest(df)

# '''Algorithm function, lookback is a data frame parsed to function continuously until end of initial dataframe is reached.'''

# def logic(account, lookback):
#     try:
#         today = len(lookback)-1
#         if(today > training_period): 
#             price_moving_average = lookback['close'].rolling(window=training_period).mean()[today]  # update PMA
#             if(lookback['close'][today] < price_moving_average):
#                     if(account.buying_power > 0):
#                         account.enter_position('long', account.buying_power, lookback['close'][today])
#             else:
#                 if(lookback['close'][today] > price_moving_average):
#                         for position in account.positions:
#                                 account.close_position(position, 1, lookback['close'][today])
#     except Exception as e:
#         print(e)
#     pass  


# # Handles lookback errors in beginning of dataset

# def logic2(account, lookback):
#     try:
#         today = len(lookback)-1
#         try:
#             yesterday = len(lookback)-2
#         except:
#             pass
#         if(today > training_period): 
#             long_price_moving_average = lookback['close'].rolling(window=long_training_period).mean()[today]  # update long average
#             short_price_moving_average = lookback['close'].rolling(window=training_period).mean()[today]  # update short average
#             yesterday_long_price_moving_average = lookback['close'].rolling(window=long_training_period).mean()[yesterday]  # yesterday long average
#             yesterday_short_price_moving_average = lookback['close'].rolling(window=training_period).mean()[yesterday]  # yesterday short average
#             volumn_moving_average = lookback['volume'].rolling(window=training_period).mean()[today]  # update VMA

#             if(yesterday_short_price_moving_average < yesterday_long_price_moving_average and short_price_moving_average >= long_price_moving_average):
#                 #if(lookback['volume'][today] > volumn_moving_average):
#                     if(account.buying_power > 0):
#                         account.enter_position('long', account.buying_power, lookback['close'][today])
#                         #print("bought at" + str(lookback["date"][today]))
#             else:
#                 if(yesterday_long_price_moving_average < yesterday_short_price_moving_average and long_price_moving_average >= short_price_moving_average):
#                     #if(lookback['volume'][today] < volumn_moving_average):
#                         for position in account.positions:
#                                 account.close_position(position, 1, lookback['close'][today])
#                                 #print("sold at" + str(lookback["date"][today]))
#     except Exception as e:
#         print(e)
#     pass  # Handles lookback errors in beginning of dataset


# if __name__ == "__main__":
#     backtest.start(100, logic2)
#     backtest.results()
#     backtest.chart()
