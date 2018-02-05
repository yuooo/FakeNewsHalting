# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:58:49 2017

@author: jessicahoffmann
"""

import heapq
import numpy as np

#%% Preprocessing functions

"""
tab_selection[k_infection] = 
    - 0 if never selected
    - t_selection if selected
"""

def EmptyFunc():
    return 0
    
def IsAlreadySelected(k_infection, tab_selection):
    return tab_selection[k_infection] != 0
    
def ValueChoice(k_infection, t_time, tab_selection, sum_infection):
    t_selection = tab_selection[k_infection]
    return sum_infection[k_infection, t_selection] - sum_infection[k_infection, t_time]
    
def CreateSum(ikt):
    k = len(ikt)
    t = len(ikt[0])
    sum_infection = np.array([[0]*(t+1) for _ in range(k)])
    for i_t in range(t):
        for i_k in range(k):
            sum_infection[i_k, i_t + 1] = sum_infection[i_k, i_t] + ikt[i_k][i_t]
    return sum_infection
 
"""
heap_infection[t] = heap of [-total_number_of_infected_people_until_time_t, k_infection]
"""   
def SortAll(sum_infection):
    t_infinity = len(sum_infection[0,:])
    n_infections = len(sum_infection)
    heap_infection = [[[-sum_infection[i_infection, t], i_infection] 
                        for i_infection in xrange(n_infections)] 
                        for t in xrange(t_infinity)]
    for t in xrange(t_infinity):
        heapq.heapify(heap_infection[t])
#        print heap_infection
    return heap_infection

""" 
Standard way of making a max-heap in python is stocking -elt in a min-heap.
"""
def GetMaxInfectionValueAtT(heap_infection, t):
    return -heap_infection[t][0][0]

##%% Main DP algo
#
#def OptimalHalting(sum_infection, heap_infection, budget):
#    t_infinity = len(heap_infection)
#    n_infections = len(heap_infection[0])
#    tab_selection = [-1]*n_infections
#    
#    policy = np.array([[-1]*t_infinity] for _ in xrange(budget))
#    
#    # Pick the best choices, time by time
#    for t in xrange(t_infinity):
#        choices_at_t = [[]]*budget
#        # Get the best choices at time t
#        for i_budget in xrange(budget):
#            # Check heap not empty
#            if heap_infection[t]:
#                choices_at_t[i_budget] = heapq.heappop(heap_infection[t])
#            else:
#                print "All nodes selected at time {} during r-best selection.".format(t)
#                return
#        # Compute the conflicts
#        conflicts = [heap_elt[1] for heap_elt in choices_at_t if tab_selection[heap_elt[1]] != 0]
#        
#        # Solve the conflicts
#        while conflicts:
#            curr_conflict = conflicts.pop()
#            infection_conflict = curr_conflict
#            t_conflict = tab_selection[infection_conflict]
#            value_next_best_t = GetMaxInfectionValueAtT(heap_infection, t)
#            value_next_best_t_conflict = GetMaxInfectionValueAtT(heap_infection, t_conflict)
#            
#            value_switch = value_next_best_t_conflict - ValueChoice(
#                            infection_conflict, t, tab_selection, sum_infection)
#            
#            if value_next_best_t >= value_switch:
#                # No switch
#                tab_selection[infection_conflict]
#        
#    
#    return

#%%
def HasBeenChosen(i_infection, tab_selection):
    return tab_selection[i_infection] != -1
    
def GetConflicts(dico_conflict, i_infection, t):
    l_conflict = []
    curr_i, curr_t = i_infection, t
    while (curr_i, curr_t) in dico_conflict:
        curr_i, curr_t = dico_conflict[(curr_i, curr_t)]
        l_conflict.append((curr_i, curr_t))
    return l_conflict
    
def NConflicts(dico_conflict, i_infection, t):
    n_conflict = 0
    curr_i, curr_t = i_infection, t
    while (curr_i, curr_t) in dico_conflict:
        curr_i, curr_t = dico_conflict[(curr_i, curr_t)]
        n_conflict += 1
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
        # Remove the already chosen infections from the heap
        while (heap_infection[t_conflict] and HasBeenChosen(heap_infection[t_conflict][0][2], tab_selection)):
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
        dico_conflict[(i_infection, t)] = (i_conflict, t_conflict)
        
        return gain

def PopHeapUntilNotChosenAtT(heap, tab_selection, t_curr):
    while (heap and 0 <= tab_selection[heap[0][2]] <= t_curr):
        heapq.heappop(heap)

def OptimalHalting(sum_infections, dico_conflict, budget):
    # Init
    t_max = len(sum_infections[0,:])
    n_infection = len(sum_infections)
    heap_infection = [[] for _ in range(t_max)]
    tab_selection = [-1]*t_max
    total_gain = 0
    gains = np.zeros((n_infection, t_max))
    dico_conflict = {}
    
    # Compute from the end
    for t in reversed(range(t_max)):
        # Compute all gains at time t
        for i_infection in range(n_infection):
            gains[i_infection, t] = Gain(i_infection, t, sum_infections, dico_conflict, heap_infection, tab_selection)
            n_conflicts = NConflicts(dico_conflict, i_infection, t)
            
        # Fill the heap at time t
        heap_infection[t] = [[- gains[i, t], n_conflicts, i] for i in xrange(n_infection)]
        heapq.heapify(heap_infection[t])
        
        # Kill budget epidemics
        for i_budget in xrange(budget):
            # Get best infection to kill
            [val_best_t, n_conflicts_t, i_best_t] = heapq.heappop(heap_infection[t])
            
            # Update the table of selected infections to incorporate the conflicts
            l_conflict = GetConflicts(dico_conflict, i_best_t, t)
            for conf in l_conflict:
                i_conf, t_conf = conf
                tab_selection[i_conf] = t_conf
        
            # Update all the heaps
            for t_1 in xrange(t, t_max):
                # Remove epidemics which are already selected
                PopHeapUntilNotChosenAtT(heap_infection[t_1], tab_selection, t_1)
                
                # Make sure the values are still up-to-date
                while heap_infection[t_1]:
                    [val_best_t_1, n_conflicts_t_1 , i_best_t_1] = heap_infection[t_1]
                    updated_val = Gain(i_best_t_1, t_1, sum_infections, dico_conflict, heap_infection, tab_selection)
                    if updated_val == val_best_t_1:
                        break
                    else :
                        heapq.heapreplace(heap_infection[t_1], 
                                          [updated_val, NConflicts(dico_conflict, i_best_t_1, t_1) , i_best_t_1])
                                          
    return total_gain, tab_selection


   