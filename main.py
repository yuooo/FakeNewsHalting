from main_fake_news_halt import *
import time
import math

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

#%% SLICING THE DATA
# We slice the time by intervals of 10min = 600s
tau = 600
t_max = int(math.ceil(max_total/tau))

ikt = np.zeros((n_infections, t_max))

def Slice(data, tau):
    for i_infection in xrange(n_infections):
        n_reshare_in_slice = 0
        i_slice = 1
        for timestamp in data[i_infection]:
            if timestamp > i_slice*600:
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
print "Slicing took {} s.".format(end - start)

#%% CREATING THE PARTIAL SUMS
start = time.time()
Ikt = CreateSum(ikt)
end = time.time()
print "Creating the partial sums took {} s.".format(end - start)

#%%  
budget = 1

start = time.time()
gain_optimal, tab_optimal = OptimalHalting(Ikt, budget)
end = time.time()
print "Optimal Halting took {} s.".format(end - start)
print "Optimal had a gain of: {}".format(gain_optimal)

start = time.time()
gain_greedy, tab_greedy = GreedyHalting(Ikt, budget)
end = time.time()
print "Greedy Halting took {} s.".format(end - start)
print "Greedy had a gain of: {}".format(gain_greedy)

#%%

def ComputeTotal(tab, Ikt):
    gain = 0
    for i in range(len(tab)):
        gain += Ikt[i, tab[i]]
    return gain
print ComputeTotal(tab_optimal, Ikt), gain_optimal
print ComputeTotal(tab_greedy, Ikt), gain_greedy

