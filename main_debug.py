# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:00:53 2018

@author: jessicahoffmann
"""

#import os
#os.chdir("/Users/jessicahoffmann/Desktop/Cours/UTAustin/Research/FakeNews")
import time
import math
import matplotlib.pyplot as plt
import heapq
import numpy as np

#%% main_halt
def CreateSum(ikt):
    k = len(ikt)
    t = len(ikt[0])
    sum_infection = np.array([[0]*(t+1) for _ in range(k)])
    for i_k in range(k):
        for i_t in reversed(range(t)):
            sum_infection[i_k, i_t] = sum_infection[i_k, i_t + 1] + ikt[i_k][i_t]
    return sum_infection
    
def PrintEveryN(t, n):
    if ((t % n) == 0):
        print "\n\nt: {}".format(t)
    

#%%
def HasBeenChosen(i_infection, tab_selection):
    print "HasBeenChosen on infection {} called".format(i_infection)
    return tab_selection[i_infection] != -1
    
def GetConflicts(dico_conflict, i_infection, t):
    print "GetConflicts on infection {} at {} called".format(i_infection, t)
    l_conflict = []
    curr_i, curr_t = i_infection, t
    while (curr_i, curr_t) in dico_conflict:
        curr_i, curr_t = dico_conflict[(curr_i, curr_t)]
        l_conflict.append((curr_i, curr_t))
    return l_conflict
    
def NConflicts(dico_conflict, i_infection, t):
    print "NConflicts on infection {} at {} called".format(i_infection, t)
    n_conflict = 0
    curr_i, curr_t = i_infection, t
    while (curr_i, curr_t) in dico_conflict:
        print "creating conflict: infection {} at {}.".format(curr_i, curr_t)
        curr_i, curr_t = dico_conflict[(curr_i, curr_t)]
        print "resolving conflict: infection {} at {}.".format(curr_i, curr_t)
        n_conflict += 1
    return n_conflict
    
#%%
    
"""
This function calculates how much we gain by killing an epidemic i_infection at
time t. In particular, it resolves the eventual conflicts as needed.
"""
def Gain(i_infection, t, sum_infections, dico_conflict, heap_infection, tab_selection):
    print "Gain on infection {} at {} called".format(i_infection, t)
    if not(HasBeenChosen(i_infection, tab_selection)):
        return -sum_infections[i_infection, t]
    else:
        t_conflict = tab_selection[i_infection]
        # Remove the already chosen infections from the heap
        while (heap_infection[t_conflict] and 0 <= tab_selection[heap_infection[t_conflict][0][2]] <= t_conflict):
            print "Gain while loop of pop() on infection {} at {} called, checking the heap at {}.".format(i_infection, t, t_conflict)
            heapq.heappop(heap_infection[t_conflict])
        
        # This infection has therefore never been chosen
        [gain_conflict, n_conflict, i_conflict] = heap_infection[t_conflict][0]

        # Make sure the infection at the time of conflict is not the one we're considering killing
        if i_conflict == i_infection:
            [gain_conflict, n_conflict, i_conflict] = heap_infection[t_conflict][1]
        
        gain = -(sum_infections[i_infection, t] - sum_infections[i_infection, t_conflict]) + gain_conflict
#        print "gain conflict : {}".format(gain_conflict)
#        print "i : {}, t : {}, sum : {}".format(i_infection, t, sum_infections[i_infection, t])
#        print "i_conflict : {}, t_conflict : {}, sum_conflict : {}".format(i_conflict, t_conflict, sum_infections[i_infection, t_conflict])

        # add the new conflict if this is selected
        print "Gain update dico_conflict on infection {} at {} called, conflict with {} at {}.".format(i_infection, t, i_conflict, t_conflict)
        dico_conflict[(i_infection, t)] = (i_conflict, t_conflict)
        
        return gain

"""
heap_infection[t] = heap of [-total_number_of_infected_people_until_time_t, n_conflicts, i_infection].
Standard way of making a max-heap in python is stocking -elt in a min-heap.
"""   
def PopHeapUntilNotChosenAtT(heap, tab_selection, t_curr):
    print "PopHeapUntilNotChosenAtT at {} called".format(t_curr)
    while (heap and 0 <= tab_selection[heap[0][2]] <= t_curr):
        heapq.heappop(heap)

def OptimalHalting(sum_infections, budget):
    # Init
    t_max = len(sum_infections[0,:])
    n_infection = len(sum_infections)
    heap_infection = [[] for _ in range(t_max)]
    tab_selection = [-1]*n_infection
    total_gain = 0
    gains = np.zeros((n_infection, t_max))
    dico_conflict = {}
    
    # Compute from the end
    for t in reversed(range(t_max)):
#        PrintEveryN(t, 1)
        # Compute all gains at time t
        for i_infection in range(n_infection):
            gains[i_infection, t] = Gain(i_infection, t, sum_infections, dico_conflict, heap_infection, tab_selection)
            n_conflicts = NConflicts(dico_conflict, i_infection, t)
            
        # Fill the heap at time t
        print "OptimalHalting: Filling heap at {} called".format(t)
        heap_infection[t] = [[gains[i, t], n_conflicts, i] for i in xrange(n_infection)]
        heapq.heapify(heap_infection[t])
        
        # Kill budget epidemics
        for i_budget in xrange(budget):
            # Get best infection to kill
            print "OptimalHalting: killing best choice at {} called for budget {}.".format(t, i_budget)
            [val_best_t, n_conflicts_t, i_best_t] = heapq.heappop(heap_infection[t])
            tab_selection[i_best_t] = t
            total_gain += val_best_t
            
            # Update the table of selected infections to incorporate the conflicts
            print "OptimalHalting: update selected infections at {} called for budget {}.".format(t, i_budget)
            l_conflict = GetConflicts(dico_conflict, i_best_t, t)
            for conf in l_conflict:
                i_conf, t_conf = conf
                tab_selection[i_conf] = t_conf
        
            # Update all the heaps
            for t_1 in xrange(t, t_max):
                # Remove epidemics which are already selected
                print "OptimalHalting: pop heaps at {} called for budget {}.".format(t, i_budget)
                PopHeapUntilNotChosenAtT(heap_infection[t_1], tab_selection, t_1)
                
                # Make sure the values are still up-to-date
                while heap_infection[t_1]:
                    print "OptimalHalting: update maximum until stable at {} called for budget {}.".format(t, i_budget)
                    [val_best_t_1, n_conflicts_t_1, i_best_t_1] = heap_infection[t_1][0]
                    updated_val = Gain(i_best_t_1, t_1, sum_infections, dico_conflict, heap_infection, tab_selection)
                    if updated_val == val_best_t_1:
                        break
                    else :
                        heapq.heapreplace(heap_infection[t_1], 
                                          [updated_val, NConflicts(dico_conflict, i_best_t_1, t_1) , i_best_t_1])
                                          
    return total_gain, tab_selection

#%% Greedy algo to compare
def GreedyHalting(sum_infections, budget):
    # Init
    t_max = len(sum_infections[0,:])
    n_infection = len(sum_infections)
    total_gain = 0
    tab_selection = [-1]*n_infection
    
    # core
    for t in range(t_max):
        heapt = [[-sum_infections[k, t], k] for k in xrange(n_infection)]
        heapq.heapify(heapt)
        for _ in xrange(budget):
            [gain, i_infection] = heapq.heappop(heapt)
            while HasBeenChosen(i_infection, tab_selection):
                [gain, i_infection] = heapq.heappop(heapt)
            tab_selection[i_infection] = t
            total_gain += gain
    return total_gain, tab_selection
   

#%% LOADING THE DATA - this takes about 10s
start = time.time()
is_first_line = True
n_lines = 0
max_total = -1
n_infections = -1
data = []
with open("spreaddata.csv", "r") as input_file: 
    for line in input_file :
        n_lines += 1
        if is_first_line:
            is_first_line = False
            continue
        timestamp, _ = map(float, line.split(','))
        if timestamp == 0:
            n_infections+= 1
            data.append([])
        data[n_infections].append(timestamp)
        max_total = max(max_total, timestamp)
end = time.time()
print "Loading took {} s.".format(end - start)

print "Max total: {}".format(max_total)

#%% SLICING THE DATA
# We slice the time by intervals of 10min = 600s
tau = 100000
t_max = int(math.ceil(max_total/tau))
print "t_max: {}".format(t_max)

ikt = np.zeros((n_infections, t_max))

def Slice(data, tau):
    for i_infection in xrange(n_infections):
        n_reshare_in_slice = 0
        i_slice = 1
        for timestamp in data[i_infection]:
            if timestamp > i_slice*tau:
                ikt[i_infection, i_slice - 1] = n_reshare_in_slice
                i_slice += 1
                n_reshare_in_slice = 0
            n_reshare_in_slice += 1
        ikt[i_infection, i_slice - 1] = n_reshare_in_slice
    return ikt

#%% 
start = time.time()
ikt = Slice(data, tau)
end = time.time()
print "Slicing took {} s.\n\n".format(end - start)


#%% CREATING THE PARTIAL SUMS
start = time.time()
Ikt = CreateSum(ikt)
end = time.time()
print "Creating the partial sums took {} s.\n\n".format(end - start)

#%%
#print Ikt[:, 131]

#%%  
budgets = np.linspace(1, (n_infections) // t_max, 20)
#budget = 10
res_optimal = []
res_greedy = []

for r in budgets:
    budget = int(r)
    start = time.time()
    gain_optimal, tab_optimal = OptimalHalting(Ikt, budget)
    end = time.time()
    print "Optimal Halting took {} s for budget {}.".format(end - start, budget)
    print "Optimal had a gain of: {}, for budget {}.".format(gain_optimal, budget)
    
    start = time.time()
    gain_greedy, tab_greedy = GreedyHalting(Ikt, budget)
    end = time.time()
    print "Greedy Halting took {} s for budget {}.".format(end - start, budget)
    print "Greedy had a gain of: {}, for budget {}.".format(gain_greedy, budget)
    
    res_optimal.append(-gain_optimal)
    res_greedy.append(-gain_greedy)

##%% Plot
##print res_greedy
##print res_optimal
#
##plt.plot(res_greedy)
##plt.plot(res_optimal)
#plt.close()
#
#diff = [res_optimal[i] - res_greedy[i] for i in range(len(res_greedy))]
#news_killed = [r*t_max*100/n_infections for r in budgets[:len(res_greedy)]]
#
#plt.plot(news_killed, diff)
#plt.title("Difference between the optimal algorithm \nand the greedy baseline as a function of the budget.")
#plt.ylabel("News exposure.")
#plt.xlabel("Budget in percent of the news.")
#
##%%
#plt.close()
#total_exposure = 0
#for infection in Ikt:
#    total_exposure += infection[0]
#    
#print "total_exposure: {}".format(total_exposure)
#
#opt = [opti*100/total_exposure for opti in res_optimal]
#greed = [greedi*100/total_exposure for greedi in res_greedy]
#
#plt.plot(news_killed, opt, "r")
#plt.plot(news_killed, greed, "b")
#plt.title("Percent of news exposure avoided for both optimal \n and greedy algorithms as a function of the budget.")
#plt.ylabel("Percent of news exposure.")
#plt.xlabel("Budget in percent of the news.")
#
##%%
#
#def ComputeTotal(tab, Ikt):
#    gain = 0
#    for i in range(len(tab)):
#        gain += Ikt[i, tab[i]]
#    return gain
#print ComputeTotal(tab_optimal, Ikt), gain_optimal
#print ComputeTotal(tab_greedy, Ikt), gain_greedy
#
