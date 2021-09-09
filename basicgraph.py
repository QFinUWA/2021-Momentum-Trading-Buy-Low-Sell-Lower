import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('ezgraph.csv')
# plt.plot(df["Strategy"].values.tolist(), df["Coin"].values.tolist())


print(df)
print(df.columns)
#plot bar graph Strategy and Coin from df
plt.bar(df["Coin"].values.tolist(), df["Strategy"].values.tolist())
# plt.xlabel('Strategy')
# plt.ylabel('Coin')
# plt.title('Strategy vs Coin')
plt.show()
print("huh")