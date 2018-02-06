# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:41:02 2018

@author: jessicahoffmann
"""

import matplotlib.pyplot as plt
import math
import numpy as np
import time

#%%
data = []

is_first_line = True
with open("spreadindex.csv", "r") as input_file: 
    for line in input_file :
        if is_first_line:
            is_first_line = False
            continue
        start, end = map(int, line.split(','))
        data.append(end - start + 1)
        
#%%
        
print data[1:10]
print len(data)


#%%
n_data = len(data)
plt.close()
x = xrange(n_data)
logdata = [math.log(y) for y in data]

data.sort()
plt.plot(x, logdata, "+")
plt.show()

#%% budget needed
plt.close()
budget = np.array([0]*(n_data + 1))
for i in range(1, n_data + 1):
    budget[i] = budget[i-1] + data[n_data - i]
    
#print sum(data)
#print budget[-1], budget[n_data - 1]
#print budget[-2]
#print budget[:10]
budget = budget * 100 /budget[-1]

tresh = np.linspace(0, 100, 21)
res = [-1]*len(tresh)
k_tresh = 0
for i in range(n_data + 1):
    if k_tresh >= len(tresh):
        break
    if budget[i] > tresh[k_tresh]:
        res[k_tresh] = i
        print "{} is for tresh {}".format(i, tresh[k_tresh])
        k_tresh += 1

res = np.array(res)
res = res * 100 / float(n_data)

#%%
plt.close()
plt.plot(res, tresh, "r*")
plt.title("Exposure prevented as a function of the budget")
plt.ylabel("Percent of the news exposure.")
plt.xlabel("Budget in percent of the news.")
axes = plt.gca()
axes.set_xlim([0,100])

#%%
print tresh
print res

#%%
print sum(data), len(data)

#%%
start = time.time()
is_first_line = True
n_lines = 0
max_total = -1
n_infections = 0
data2 = [[]]
with open("spreaddata.csv", "r") as input_file: 
    for line in input_file :
        n_lines += 1
        if is_first_line:
            is_first_line = False
            continue
        timestamp, _ = map(float, line.split(','))
        if timestamp == 0:
            n_infections+= 1
            data2.append([])
        data2[n_infections].append(timestamp)
        max_total = max(max_total, timestamp)
end = time.time()
        
print max_total, n_lines, n_infections
print "it took {} s.".format(end- start)

#%%
print max(data), max(max(data2))

#%%

