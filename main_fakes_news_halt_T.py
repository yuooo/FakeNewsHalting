# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:59:48 2017

@author: jessicahoffmann
"""

import unittest
from main_fake_news_halt import *

class TestImport(unittest.TestCase):
    def testA(self):
        self.assertEqual(EmptyFunc(), 0)
        
        
class TestHelpers(unittest.TestCase):
    def testCreateSum(self):
        ikt = [[2,5,0,3], [0,0,0,10], [0,0,4,2], [20,0,0,0], [2,8,7,7], [0,20,0,0], [0,2,4,8]]
        sol = [[10,8,3,3, 0], [10,10,10,10, 0], [6,6,6,2, 0], [20,0,0,0, 0], [24,22,14,7, 0], [20,20,0,0, 0], [14,14,12,8, 0]]
        pot_sol = CreateSum(ikt)    
#        print pot_sol
        k = len(sol)
        t = len(sol[0])
        for i_lig in range(k):
            for i_col in range(t):
#                print i_lig, i_col
                self.assertEqual(sol[i_lig][i_col], pot_sol[i_lig][i_col])
            

    def testHasBeenChosen(self):
        tab_selection = [0, -1, 3, -1]
        sol = [True, False, True, False]
        for i in range(len(tab_selection)):
            self.assertEqual(HasBeenChosen(i, tab_selection), sol[i])
        
    def testGetConflicts(self):
        dico_conflict = {(1, 3) : (2, 4, 1), 
                         (1, 2) : (2, 4, 1), 
                         (3, 2) : (2, 3, 1), 
                         (1, 1) : (2, 4, 1), 
                         (2, 1) : (3, 2, 2),
                         (3, 1) : (2, 3, 1)}
        l_1_3 = [(2, 4, 1)]
        l_1_4 = []
        l_2_1 = [(3, 2, 2), (2, 3, 1)]
        self.assertListEqual(l_1_3, GetConflicts(dico_conflict, 1, 3))
        self.assertListEqual(l_1_4, GetConflicts(dico_conflict, 1, 4))
        self.assertListEqual(l_2_1, GetConflicts(dico_conflict, 2, 1))
        
    def testNConflicts(self):
        dico_conflict = {(1, 3) : (2, 4, 1), 
                         (1, 2) : (2, 4, 1), 
                         (3, 2) : (2, 3, 1), 
                         (1, 1) : (2, 4, 1), 
                         (2, 1) : (3, 2, 2),
                         (3, 1) : (2, 3, 1)}
        n_1_3 = 1
        n_1_4 = 0
        n_2_1 = 2
        self.assertEqual(n_1_3, NConflicts(dico_conflict, 1, 3))
        self.assertEqual(n_1_4, NConflicts(dico_conflict, 1, 4))
        self.assertEqual(n_2_1, NConflicts(dico_conflict, 2, 1))
        
class TestCore(unittest.TestCase):
    def testPopHeapUntilNotChosenAtT(self):
        tab_selection = [-1, 3, 7, 10, -1]
        heap1 = [[-3, 0, 0], [-40, 0, 1], [-20, 0, 2], [-10, 0, 3], [-2, 0, 4]]
        heap2 = list(heap1)
        heap3 = list(heap1)
        heapq.heapify(heap1)
        heapq.heapify(heap2)
        heapq.heapify(heap3)
        PopHeapUntilNotChosenAtT(heap1, tab_selection, 7)
        [val, conflict, i_infection] = heap1[0]
        self.assertEqual(i_infection, 3)
        self.assertEqual(val, -10)
        PopHeapUntilNotChosenAtT(heap2, tab_selection, 1)
        [val, conflict, i_infection] = heap2[0]
        self.assertEqual(i_infection, 1)
        self.assertEqual(val, -40)
        PopHeapUntilNotChosenAtT(heap3, tab_selection, 11)
        [val, conflict, i_infection] = heap3[0]
        self.assertEqual(i_infection, 0)
        self.assertEqual(val, -3)
        
    def testGain(self):
        sum_infections = np.array([[10, 6, 6, 6],
                                   [20, 14, 10, 4],
                                   [40, 40, 40, 0],
                                   [10, 8, 4, 4], 
                                   [10, 4, 4, 4]])
        n_infection = len(sum_infections)
        t_max = len(sum_infections[0, :]) 
#        print "t_max: {}".format(t_max)
        heap_infection = [[] for _ in xrange(t_max)]
        heap_infection[t_max - 1] = [[-4, 0, 1], [0, 0, 2], [-4, 0, 3], [-4, 0, 4]]
        heap_infection[t_max - 2] = [[-4, 1, 0], [-10, 0, 1], [-4, 0, 3], [-4, 0, 4]]
        heapq.heapify(heap_infection[t_max - 1])
        heapq.heapify(heap_infection[t_max - 2])
        dico_conflict = {(1, 2) : (2, 3, 1)}
        tab_selection = [3, -1, 2, -1, -1]         
        sol_gains = [-4, -14, -10, -8, -4]
        t = 1
        for i_infection in xrange(n_infection):
#            print 
#            print "i_infection : {}".format(i_infection)
#            print dico_conflict
            self.assertEqual(Gain(i_infection, t, sum_infections, dico_conflict, heap_infection, tab_selection), 
                             sol_gains[i_infection])
        self.assertTrue((0, 1) in dico_conflict)
        self.assertTrue(dico_conflict[(0, 1)] == (1, 3, 1))
        self.assertTrue((2, 1) in dico_conflict)
        self.assertTrue(dico_conflict[(2, 1)] == (1, 2, 2))    
        
    
    def testOptimalHalting(self):
        sum_infections = np.array([[10, 6, 6, 6],
                                   [20, 14, 10, 4],
                                   [40, 40, 40, 0],
                                   [10, 8, 4, 4], 
                                   [10, 4, 4, 4]])
        budget = 1
        gain, tab = OptimalHalting(sum_infections, budget)
        gain_sol = -(6 + 40 + 8 + 20)
        tab_sol = [3, 0, 2, 1, -1]
#        print gain
#        print tab
        self.assertEqual(gain, gain_sol)
        self.assertListEqual(tab, tab_sol)
        
    def testOneStepOptimalHalting(self):
        sum_infections = np.array([[10, 8, 7, 6],
                                   [20, 14, 10, 5],
                                   [42, 41, 40, 0],
                                   [14, 8, 4, 4], 
                                   [12, 7, 3, 1]])
        gain_sol = [[8, 7, 5, 6],
                    [14, 14, 10, 5],
                    [7, 11, 40, 0],
                    [13, 8, 4, 4],
                    [12, 7, 3, 1]]
        budget = 1
        t_max = len(sum_infections[0,:])
        n_infection = len(sum_infections)
        heap_infection = [[] for _ in range(t_max)]
        tab_selection = [-1]*n_infection
        total_gain = 0
        gains = np.zeros((n_infection, t_max))
        dico_conflict = {}
        # t = 3
        total_gain += OneStepOptimalHalting(sum_infections, budget, 3, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -6)
        sol_tab_selection = [3, -1, -1, -1, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-5, 0, 1]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
        # t = 2
        total_gain += OneStepOptimalHalting(sum_infections, budget, 2, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -46)
        sol_tab_selection = [3, -1, 2, -1, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-5, 0, 1], [-10, 0, 1]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
        # t = 1
        total_gain += OneStepOptimalHalting(sum_infections, budget, 1, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -60)
        sol_tab_selection = [3, 1, 2, -1, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-4, 0, 3], [-5, 1, 0], [-8, 0, 3]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
        # t = 0
        total_gain += OneStepOptimalHalting(sum_infections, budget, 0, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -74)
        sol_tab_selection = [3, 0, 2, 1, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-1, 0, 4], [-3, 0, 4], [-7, 0, 4], [-13, 1, 3]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
            
            
    def testOneStepOptimalHalting_loops(self):
        sum_infections = np.array([[1, 1, 1, 1, 1],
                                   [32, 32, 4, 4, 4],
                                   [16, 16, 16, 3, 3],
                                   [10, 10, 10, 10, 2], 
                                   [5, 5, 5, 5, 5],
                                   [1, 1, 1, 1, 1]])
        budget = 1
        t_max = len(sum_infections[0,:])
        n_infection = len(sum_infections)
        heap_infection = [[] for _ in range(t_max)]
        tab_selection = [-1]*n_infection
        total_gain = 0
        gains = np.zeros((n_infection, t_max))
        dico_conflict = {}
        # t = 4
        total_gain += OneStepOptimalHalting(sum_infections, budget, 4, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -5)
        sol_tab_selection = [-1, -1, -1, -1, 4, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-4, 0, 1]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
        # t = 3
        total_gain += OneStepOptimalHalting(sum_infections, budget, 3, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -15)
        sol_tab_selection = [-1, -1, -1, 3, 4, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-4, 0, 1], [-4, 0, 1]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
        # t = 2
        total_gain += OneStepOptimalHalting(sum_infections, budget, 2, dico_conflict, 
                                            heap_infection, tab_selection, gains, n_infection, t_max)
        self.assertEqual(total_gain, -28)
        sol_tab_selection = [-1, -1, -1, 3, 4, -1]
        self.assertListEqual(tab_selection, sol_tab_selection)
        heaps_top = [[-2, 0, 1], [-2, 0, 1], [-2, 0, 1]]
        for i in range(len(heaps_top)):
            self.assertListEqual(heaps_top[i], heap_infection[t_max - 1 -i][0])
        
        
    
    def testGreedyHalting(self):
        sum_infections = np.array([[10, 6, 6, 6],
                                   [20, 14, 10, 4],
                                   [40, 40, 40, 0],
                                   [10, 8, 4, 4], 
                                   [10, 4, 4, 4]])
        budget = 1
        gain, tab = GreedyHalting(sum_infections, budget)
#        print gain, tab
        gain_sol = -(40 + 14 + 6 + 4)
        tab_sol = [2, 1, 0, 3, -1]
        
        self.assertEqual(gain, gain_sol)
        self.assertListEqual(tab, tab_sol)
        
if __name__ == '__main__':
    unittest.main()
