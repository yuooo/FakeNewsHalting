# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:45:18 2018

@author: jessicahoffmann
"""
import numpy as np
import heapq

A = [[1,2], [3,4]]
A_np = np.array(A)

print A
print A_np
print A_np[0, :]
print A_np[:, 1]

H = []
H.append(heapq.heapify([1]))
H.append(heapq.heapify([5,4]))

a = [1]
b = [5,4]

heapq.heapify(a)
heapq.heapify(b)

H.append(a)
H.append(b)

print H
print H[3]
print heapq.heappop(H[3])

c = (1,2)
print c[1]

#%%
d = 7
print 0<= d < 6

#%% Plot
res_greedy = [284063, 776626, 1002569]
res_optimal = [308387.0, 808802.0, 1035433.0]

#plt.plot(news_killed, res_greedy)
#plt.plot(news_killed, res_optimal)
#plt.show()
#plt.close()
#
#diff = [res_optimal[i] - res_greedy[i] for i in range(len(res_greedy))]
news_killed = [r*t_max*100.0/n_infections for r in budgets[:len(res_greedy)]]
#
#plt.plot(news_killed, diff)
#plt.title("Difference between the optimal algorithm \nand the greedy baseline as a function of the budget.")
#plt.ylabel("News exposure.")
#plt.xlabel("Budget in percent of the news.")
#
##%%
#plt.close()
total_exposure = sum(ikt[ikt > 0])
    
print "total_exposure: {}".format(total_exposure)

opt = [opti*100.0/total_exposure for opti in res_optimal]
greed = [greedi*100.0/total_exposure for greedi in res_greedy]

plt.plot(news_killed, opt, "r", label = "Optimal Algorithm")
plt.plot(news_killed, greed, "b", label = "Greedy heuristic")
plt.title("Percent of news exposure avoided for both optimal \n and greedy algorithms as a function of the budget.")
plt.ylabel("Percent of news exposure.")
plt.xlabel("Budget in percent of the news.")
plt.legend(bbox_to_anchor=(0.96,0.3))
plt.show()