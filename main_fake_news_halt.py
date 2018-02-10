# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:58:49 2017

@author: jessicahoffmann
"""

import heapq
import numpy as np
Inf = float('Inf')

#%% Preprocessing functions

"""
tab_selection[k_infection] = 
    - -1 if never selected
    - t_selection if selected
"""

def EmptyFunc():
    return 0
    
def CreateSum(ikt):
    k = len(ikt)
    t = len(ikt[0])
    sum_infection = np.array([[0]*(t+1) for _ in range(k)])
    for i_k in range(k):
        for i_t in reversed(range(t)):
            sum_infection[i_k, i_t] = sum_infection[i_k, i_t + 1] + ikt[i_k][i_t]
    return sum_infection
    

def Slice(data, tau, t_max, start_time):
    n_infections = len(data) - 1
    infty = 2<<30
    ikt = np.zeros((n_infections, t_max))
    
    for i_infection in xrange(n_infections):
        n_reshare_in_slice = 0
        i_slice = 1
        
        # Cannot kill an infection before it has started
        while i_slice*tau <= start_time[i_infection]:
            ikt[i_infection, i_slice - 1] = -infty
            i_slice += 1
            if i_slice > t_max:
                break
        # Fill the time slices
        for timestamp in data[i_infection]:
            real_time = timestamp + start_time[i_infection]
            # Discard timestamp before t=0
            if real_time < 0:
                continue
            
            # Keep all the lesftover reshares in the last time step
            if i_slice == t_max:
                n_reshare_in_slice += 1
                continue
            
            # Need to change slice
            if real_time >= i_slice*tau:
                ikt[i_infection, i_slice - 1] = n_reshare_in_slice
                while real_time >= i_slice*tau:
                    i_slice += 1
                    if i_slice > t_max - 1:
                        break
                n_reshare_in_slice = 0
            n_reshare_in_slice += 1
        ikt[i_infection, i_slice - 1] = n_reshare_in_slice
    return ikt
    
def ComputeTotal(tab, Ikt):
    gain = 0
    for i in range(len(tab)):
        gain += Ikt[i, tab[i]]
    return gain

    
def PrintEveryN(t, n):
    if ((t % n) == 0):
        print "t: {}".format(t)
    

#%%
def HasBeenChosen(i_infection, tab_selection):
    return tab_selection[i_infection] != -1
    
def GetConflicts(dico_conflict, i_infection, t):
    l_conflict = []
    curr_i, curr_t = i_infection, t
    while (curr_i, curr_t) in dico_conflict:
        curr_i, curr_t, n_conflict = dico_conflict[(curr_i, curr_t)]
        l_conflict.append((curr_i, curr_t, n_conflict))
    return l_conflict
    
def NConflicts(dico_conflict, i_infection, t):
    n_conflict = 0
    if (i_infection, t) in dico_conflict:
        dummy1, dummy2, n_conflict = dico_conflict[(i_infection, t)]
    return n_conflict
    
#%%
    
"""
This function calculates how much we gain by killing an epidemic i_infection at
time t. In particular, it resolves the eventual conflicts as needed.
"""
def Gain(i_infection, t, sum_infections, dico_conflict, heap_infection, tab_selection):
    if not(HasBeenChosen(i_infection, tab_selection)):
        return -sum_infections[i_infection, t]
    else:
        t_conflict = tab_selection[i_infection]
        if t_conflict <= t:
            return 0
            
        # This infection has therefore never been chosen
        [gain_conflict, n_conflict, i_conflict] = heap_infection[t_conflict][0]
        
        gain = -(sum_infections[i_infection, t] - sum_infections[i_infection, t_conflict]) + gain_conflict
#        print "gain conflict : {}".format(gain_conflict)
#        print "i : {}, t : {}, sum : {}".format(i_infection, t, sum_infections[i_infection, t])
#        print "i_conflict : {}, t_conflict : {}, sum_conflict : {}".format(i_conflict, t_conflict, sum_infections[i_infection, t_conflict])

        # add the new conflict if this is selected
        if (i_conflict, t_conflict) in dico_conflict:
            dummy1, dummy2, n_conflicts_at_t_conflict = dico_conflict[(i_conflict, t_conflict)]
            dico_conflict[(i_infection, t)] = (i_conflict, t_conflict, n_conflicts_at_t_conflict + 1)
        else:
            dico_conflict[(i_infection, t)] = (i_conflict, t_conflict, 1)
        
        return gain

"""
heap_infection[t] = heap of [-total_number_of_infected_people_until_time_t, n_conflicts, i_infection].
Standard way of making a max-heap in python is stocking -elt in a min-heap.
"""   
def PopHeapUntilNotChosenAtT(heap, tab_selection, t_curr):
    while (heap and 0 <= tab_selection[heap[0][2]] <= t_curr):
        heapq.heappop(heap)
        
def OneStepOptimalHalting(sum_infections, budget, t, dico_conflict, 
                          heap_infection, tab_selection, gains, n_infection, t_max):
    PrintEveryN(t, 100)
    total = 0
    # Compute all gains at time t
    for i_infection in range(n_infection):
        gains[i_infection, t] = Gain(i_infection, t, sum_infections, dico_conflict, 
                                     heap_infection, tab_selection)
        n_conflicts = NConflicts(dico_conflict, i_infection, t)
        
    # Fill the heap at time t
    heap_infection[t] = [[gains[i, t], n_conflicts, i] for i in xrange(n_infection)]
    heapq.heapify(heap_infection[t])
    
    # Kill budget epidemics
    for i_budget in xrange(budget):
        # Get best infection to kill
        [val_best_t, n_conflicts_t, i_best_t] = heapq.heappop(heap_infection[t])
        tab_selection[i_best_t] = t
        total+= val_best_t
        
        
        # Update the table of selected infections to incorporate the conflicts
        l_conflict = GetConflicts(dico_conflict, i_best_t, t)
        for conf in l_conflict:
            i_conf, t_conf, _ = conf
            tab_selection[i_conf] = t_conf
        
        
        # Update all the heaps
        for t_1 in reversed(xrange(t, t_max)):
            # Make sure the values are still up-to-date
            while heap_infection[t_1]:
                # Remove epidemics which are already selected
                PopHeapUntilNotChosenAtT(heap_infection[t_1], tab_selection, t_1)
                
                [val_best_t_1, n_conflicts_t_1, i_best_t_1] = heap_infection[t_1][0]
                updated_val = Gain(i_best_t_1, t_1, sum_infections, dico_conflict, heap_infection, tab_selection)
                if updated_val == val_best_t_1:
                    break
                else :
                    heapq.heapreplace(heap_infection[t_1], 
                                      [updated_val, NConflicts(dico_conflict, i_best_t_1, t_1) , i_best_t_1])
    return total

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
        total_gain += OneStepOptimalHalting(sum_infections, budget, t, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
                                          
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
   