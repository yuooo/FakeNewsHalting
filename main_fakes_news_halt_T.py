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
        sol = [[0,2,7,7,10], [0,0,0,0,10], [0,0,0,4,6], [0,20,20,20,20], [0,2,10,17,24], [0,0,20,20,20], [0,0,2,6,14]]
        pot_sol = CreateSum(ikt)    
        k = len(sol)
        t = len(sol[0])
        for i_lig in range(k):
            for i_col in range(t):
#                print i_lig, i_col
                self.assertEqual(sol[i_lig][i_col], pot_sol[i_lig][i_col])
                
    def testSortAll(self):
        sums = np.array([[0,3,7,7,10], [0,0,0,0,20], [0,0,0,4,6], [0,2,10,17,18]])
        heap_infections = SortAll(sums)
        maxima = [0, 3, 10, 17, 20]
        origin = [0,0,3,3,1]
        second_max = [0, 2, 7, 7, 18]
        for t in range(len(sums[0])):
            self.assertEqual(heap_infections[t][0][0], -maxima[t])
            self.assertEqual(heap_infections[t][0][1], origin[t])
#            print heap_infections[t][0], -maxima[t]
            self.assertEqual(heap_infections[t][1][0], -second_max[t])
            
    def testGetMaxInfectionValueAtT(self):
        sums = np.array([[0,3,7,7,10], [0,0,0,0,20], [0,0,0,4,6], [0,2,10,17,18]])
        heap_infections = SortAll(sums)
        maxt = [GetMaxInfectionValueAtT(heap_infections, t) for t in xrange(len(sums[0]))]
        maxima = [0, 3, 10, 17, 20]
        for t in range(len(sums[0])):
            self.assertEqual(maxt[t], maxima[t])

    def testHasBeenChosen(self):
        tab_selection = [0, -1, 3, -1]
        sol = [True, False, True, False]
        for i in range(len(tab_selection)):
            self.assertEqual(HasBeenChosen(i, tab_selection), sol[i])
        
    def testGetConflicts(self):
        dico_conflict = {(1, 3) : (2, 4), 
                         (1, 2) : (2, 4), 
                         (3, 2) : (2, 3), 
                         (1, 1) : (2, 4), 
                         (2, 1) : (3, 2),
                         (3, 1) : (2, 3)}
        l_1_3 = [(2, 4)]
        l_1_4 = []
        l_2_1 = [(3, 2), (2, 3)]
        self.assertListEqual(l_1_3, GetConflicts(dico_conflict, 1, 3))
        self.assertListEqual(l_1_4, GetConflicts(dico_conflict, 1, 4))
        self.assertListEqual(l_2_1, GetConflicts(dico_conflict, 2, 1))
        
    def testNConflicts(self):
        dico_conflict = {(1, 3) : (2, 4), 
                         (1, 2) : (2, 4), 
                         (3, 2) : (2, 3), 
                         (1, 1) : (2, 4), 
                         (2, 1) : (3, 2),
                         (3, 1) : (2, 3)}
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
        print "t_max: {}".format(t_max)
        heap_infection = [[] for _ in xrange(t_max)]
        heap_infection[t_max - 1] = [[-4, 0, 1], [0, 0, 2], [-4, 0, 3], [-4, 0, 4]]
        heap_infection[t_max - 2] = [[-4, 1, 0], [-10, 0, 1], [-4, 0, 3], [-4, 0, 4]]
        heapq.heapify(heap_infection[t_max - 1])
        heapq.heapify(heap_infection[t_max - 2])
        dico_conflict = {(1, 2) : (2, 3)}
        tab_selection = [3, -1, 2, -1, -1]         
        sol_gains = [-4, -14, -10, -8, -4]
        t = 1
        for i_infection in xrange(n_infection):
            print 
            print "i_infection : {}".format(i_infection)
            print dico_conflict
            self.assertEqual(Gain(i_infection, t, sum_infections, dico_conflict, heap_infection, tab_selection), 
                             sol_gains[i_infection])
        self.assertTrue((0, 1) in dico_conflict)
        self.assertTrue(dico_conflict[(0, 1)] == (1, 3))
        self.assertTrue((2, 1) in dico_conflict)
        self.assertTrue(dico_conflict[(2, 1)] == (1, 2))        
        
        
if __name__ == '__main__':
    unittest.main()
