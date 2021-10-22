import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
df = pd.read_csv("results_overnight_kane.csv")


# value = []
# for a, b in df.groupby(["Strategy_Name","Price_Window"]):
#     if(a[0] =='standard_no_volume'):
#         value.append([b["Strategy"].sum() - b["Buy and Hold"].sum(),a[1]])
# df2 = pd.DataFrame(value,columns=["Net Return","Price Window"])
# df2.to_csv("standard_no_volume.csv",index=False)

value = []
for a, b in df.groupby(["Strategy_Name","Price_Window"]):
    if(a[0] =='exp_no_volume'):
        value.append([b["Strategy"].sum() - b["Buy and Hold"].sum(),a[1]])
df2 = pd.DataFrame(value,columns=["Net Return","Price Window"])
df2.to_csv("exp_no_volume.csv",index=False)
        

# csv = []
# for a, b in df.groupby(["Strategy_Name","Price_Window"]):
#     if(a[0] =='standard'):
#         yaxis = []
#         for e,c in b.groupby(["Volume_Window"]):
#             value = pd.DataFrame()
#             value["y-axis"] = c["Strategy"] - c["Buy and Hold"]
#             yaxis.append(value["y-axis"].values.tolist())
#         arrays = [np.array(x) for x in yaxis]
#         result = [np.mean(k) for k in zip(*arrays)]
#         csv.append([sum(result),a[1]])

# df2 = pd.DataFrame(csv,columns=["Net Return","Price Window"])
# df2.to_csv("standard_price.csv",index=False) 


# csv = []
# for a, b in df.groupby(["Strategy_Name","Volume_Window"]):
#     if(a[0] =='standard'):
#         yaxis = []
#         for e,c in b.groupby(["Price_Window"]):
#             value = pd.DataFrame()
#             value["y-axis"] = c["Strategy"] - c["Buy and Hold"]
#             yaxis.append(value["y-axis"].values.tolist())
#         arrays = [np.array(x) for x in yaxis]
#         result = [np.mean(k) for k in zip(*arrays)]
#         csv.append([sum(result),a[1]])
#         print(csv)

# df2 = pd.DataFrame(csv,columns=["Net Return","Price Window"])
# df2.to_csv("standard_volume.csv",index=False)  

# value = []
# xvalues = []
# yvalues = []
# zvalues = []
# for a, b in df.groupby(["Strategy_Name"]):
#     if(a == 'standard'):
#         for e,c in b.groupby(["Price_Window","Volume_Window"]):
#             value1 = c["Strategy"].sum() - c["Buy and Hold"].sum()
#             value.append([value1,e[0],e[1]])
#             xvalues.append(e[0])
#             yvalues.append(e[1])
#             zvalues.append(value1)
# # fig = plt.figure()
# # ax = fig.add_subplot(projection="3d")
# # ax.scatter(xvalues, yvalues, zvalues)
# # plt.show()      

        

# df2 = pd.DataFrame(value,columns=["Net Return","Price Window","Volume_Window"])
# df2.to_csv("idfk.csv",index=False)  
# pivot = df2.pivot("Price Window","Volume_Window","Net Return")
# ax = sns.heatmap(pivot,cmap="RdBu")
# plt.show()

# csv = []
# for a, b in df.groupby(["Strategy_Name","Price_Window"]):
#     if(a[0] == 'Crossover moving average'):
#         yaxis = []
#         for e,c in b.groupby(["Long_Price_Window"]):
#             value = pd.DataFrame()
#             value["y-axis"] = c["Strategy"] - c["Buy and Hold"]
#             yaxis.append(value["y-axis"].values.tolist())
#         arrays = [np.array(x) for x in yaxis]
#         result = [np.mean(k) for k in zip(*arrays)]
#         csv.append([sum(result),a[1]])

# df2 = pd.DataFrame(csv,columns=["Net Return","Short Price Window"])
# df2.to_csv("crossover_short.csv",index=False)  

   