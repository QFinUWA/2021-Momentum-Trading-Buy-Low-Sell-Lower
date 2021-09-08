import pandas as pd
from pandas import DataFrame
from talib.abstract import *
import time
import numpy as np
import multiprocessing as mp

# local imports
from gemini_modules import engine

# LOGIC FUNCTIONS
LOGIC0 = {
    "name":"standard_no_volume",
    "active": True,
    "price_start_index": 0,
    "price_end_index": 25,
    "price_multiplier": 2,
    "price_index":0,
    "volume_index":0,
    "price_long_index":0,
}

LOGIC1 = {
    "name":"standard",
    "active": True,
    "price_start_index": 0,
    "price_end_index": 25,
    "price_multiplier": 2,
    "price_index":0,
    "volume_start_index": 0,
    "volume_end_index": 25,
    "volume_multiplier": 2,
    "volume_index":0,
    "price_long_index":0,
}


#Convert python dictionarys to javascripts ones for cleaner code :D
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self
LOGIC0 = AttrDict(LOGIC0)
LOGIC1 = AttrDict(LOGIC1)


price_window = None
price_window_long = None
price_array = None
volume_array = None
volume_window = None

def updateglobals(logic_function):
    global price_window,price_array,volume_array,volume_window,price_window_long
    price_array = np.array([])
    volume_array = np.array([])
    price_window = logic_function.price_index
    volume_window = logic_function.volume_index
    price_window_long = logic_function.price_long_index



def logic0(account, lookback):
    code = True


def logic1(account, lookback):
    code= True

list_of_coins = ["USDT_ADA","USDT_BTC","USDT_ETH","USDT_LTC","USDT_XRP"]

lock = mp.Lock()
def backtest_coin(results,coin,logic_function,logic):
    df = pd.read_csv("train_data/" + coin + ".csv", parse_dates=[0])
    updateglobals(logic_function)
    backtest = engine.backtest(df)
    backtest.start(1000, logic)
    lock.acquire()
    data = backtest.results()
    data.extend([coin,logic_function.name,logic_function.volume_index,logic_function.price_index,logic_function.price_long_index]) #coinname
    results.append(data)
    lock.release()


if __name__ == "__main__":
    print("Running Algorithms...")
    manager = mp.Manager()
    results = manager.list()
    starttime = time.time()
    if(LOGIC0.active):
        for price_window in range(LOGIC0.price_start_index,LOGIC0.price_end_index):
            print("LOGIC 1: COMPLETED: " + str(price_window) + " REMAINING: "+  str(LOGIC0.price_end_index) )
            LOGIC0.price_index = price_window*LOGIC0.price_multiplier
            processes = []
            for coin in list_of_coins:
                p = mp.Process(target=backtest_coin, args=(results,coin,LOGIC0,logic0))
                processes.append(p)
                p.start()
            for process in processes:
                process.join()
                processes.remove(process)
    print("Done Logic 0")
    if(LOGIC1.active):
        for price_window in range(LOGIC1.price_start_index,LOGIC1.price_end_index):
            LOGIC1.price_index = price_window*LOGIC1.price_multiplier
            for volume_window in range(LOGIC1.volume_start_index,LOGIC1.volume_end_index):
                print("LOGIC 0: COMPLETED: " + str(price_window) +":"+ str(volume_window) + " REMAINING: "+ str(LOGIC1.price_end_index) + ":"+str(LOGIC1.volume_end_index) )
                LOGIC1.volume_index = volume_window*LOGIC1.volume_multiplier
                processes = []
                for coin in list_of_coins:
                    p = mp.Process(target=backtest_coin, args=(results,coin,LOGIC1,logic1))
                    processes.append(p)
                    p.start()
                for process in processes:
                    process.join()
                    processes.remove(process)
    

    df = DataFrame(list(results),columns=["Buy and Hold","Strategy","Longs","Sells","Shorts","Covers","Stdev_Strategy","Stdev_Hold","Coin",'Strategy_Name','Volume_Window','Price_Window','Long_Price_Window'])
    df.to_csv("results.csv",index =False)
    print("Done")
    print('That took {} seconds'.format(time.time() - starttime))
