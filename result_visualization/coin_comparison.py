import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('ezgraph.csv')
# plt.plot(df["Strategy"].values.tolist(), df["Coin"].values.tolist())

                                            # 59.32,USDT_NEO
                                            # 80.5,USDT_DASH
                                            # 796.98,USDT_ADA
                                            # 2270.8,USDT_LTC
                                            # 125.37,USDT_XRP
                                            # 240.23,USDT_BTC
                                            # 843.05,USDT_ETH

# print(df)
# print(df.columns)
#plot bar graph Strategy and Coin from df
plt.bar(df["Coin"].values.tolist(), df["Strategy"].values.tolist(), color=['brown', 'green', 'blue', 'purple', 'pink', "orange", "red"])
plt.xlabel('Coin')
plt.ylabel('Strategy')
plt.title('Performance of SMA - No Volume for Each Coin')
plt.show()