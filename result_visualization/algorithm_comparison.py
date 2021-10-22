
import numpy as np
import matplotlib.pyplot as plt
  
N = 4
ind = np.arange(N) 
width = 0.11
  
neo = [116.85,
98.37,
165.34,
58.64,
]
bar1 = plt.bar(ind, neo, width, color = 'brown')
  
dash = [13.38,
122.98,
275.06,
93.35]

bar2 = plt.bar(ind+width, dash, width, color='green')
  
ada = [
    274.2,
399.7,
63.26,
561.29]

bar3 = plt.bar(ind+width*2, ada, width, color = 'blue')

ltc = [
    74.56,
1855.13,
1439.61,
2073.18]

bar4 = plt.bar(ind+width*3, ltc, width, color = 'purple')

xrp = [
    207.97,
47.56,
70.07,
112.06]

bar5 = plt.bar(ind+width*4, xrp, width, color = 'pink')

btc = [
    49.92,
-119.86,
-33.54,
-60.64]

bar6 = plt.bar(ind+width*5, btc, width, color = 'orange')

eth = [377.31,
74.39,
204.2,
377.36]

bar7 = plt.bar(ind+width*6, eth, width, color = 'red')


avg = [159.97,354.04,312, 495.32]

bar8 = plt.bar(ind+width*7, avg, width, color = 'black')

# plt.xlabel("Algorithm")
plt.ylabel('Percentage Improvement on Buy and Hold')
plt.title("Optimized Algorithm Comparison")
  
plt.xticks(ind+width+0.28,['Crossover','Exponential','SMA','SMA No Volume'])
plt.legend( (bar1, bar2, bar3,bar4, bar5, bar6,bar7,bar8), ('NEO','DASH', 'ADA',"LTC","XRP","BTC","ETH","AVERAGE") )
plt.show()