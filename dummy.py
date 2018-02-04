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