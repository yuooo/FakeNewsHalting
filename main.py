import os
#os.chdir("/Users/jessicahoffmann/Desktop/Cours/UTAustin/Research/FakeNews")
from main_fake_news_halt import *
import time
import math
import matplotlib.pyplot as plt

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
print "Slicing took {} s.".format(end - start)

#%% CREATING THE PARTIAL SUMS
start = time.time()
Ikt = CreateSum(ikt)
end = time.time()
print "Creating the partial sums took {} s.".format(end - start)

#%%
#print Ikt[:, 131]

#%%  
#budgets = np.linspace(1, (n_infections) // t_max, 20)
#budget = 10
budgets = [1]
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

#%% Plot
#print res_greedy
#print res_optimal

#plt.plot(res_greedy)
#plt.plot(res_optimal)
plt.close()

diff = [res_optimal[i] - res_greedy[i] for i in range(len(res_greedy))]
news_killed = [r*t_max*100/n_infections for r in budgets[:len(res_greedy)]]

plt.plot(news_killed, diff)
plt.title("Difference between the optimal algorithm \nand the greedy baseline as a function of the budget.")
plt.ylabel("News exposure.")
plt.xlabel("Budget in percent of the news.")

#%%
plt.close()
total_exposure = 0
for infection in Ikt:
    total_exposure += infection[0]
    
print "total_exposure: {}".format(total_exposure)

opt = [opti*100/total_exposure for opti in res_optimal]
greed = [greedi*100/total_exposure for greedi in res_greedy]

plt.plot(news_killed, opt, "r")
plt.plot(news_killed, greed, "b")
plt.title("Percent of news exposure avoided for both optimal \n and greedy algorithms as a function of the budget.")
plt.ylabel("Percent of news exposure.")
plt.xlabel("Budget in percent of the news.")

#%%

def ComputeTotal(tab, Ikt):
    gain = 0
    for i in range(len(tab)):
        gain += Ikt[i, tab[i]]
    return gain
print ComputeTotal(tab_optimal, Ikt), gain_optimal
print ComputeTotal(tab_greedy, Ikt), gain_greedy

