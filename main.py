import os
#os.chdir("/Users/jessicahoffmann/Desktop/Cours/UTAustin/Research/FakeNews")
from main_fake_news_halt import *
import time
import math
import matplotlib.pyplot as plt
import sys

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
print "n_infections", n_infections, len(data)

#%% GENERATING START TIME
# We spread our news around 5 days, with 3 peaks a day: 7am, 12pm, 6pm. The news 
# are then generated at a time given by a gaussian with standard deviation one hour,
# centered on one of these peaks. t=0 is the first day at 7am.

n_seconds_by_day = 3600*24
peaks = [0, 5*3600, 11*3600]
peaks_5_days = [peak + i*n_seconds_by_day for peak in peaks for i in range(5)]
gaussians = 3600*np.random.standard_normal(n_infections)

choose_peak = np.random.randint(0, len(peaks_5_days), n_infections)

start_time = [peaks_5_days[choose_peak[i]] + gaussians[i] for i in range(n_infections)]

#%% SLICING THE DATA
# We slice the time by intervals of 10min = 600s
tau = 10000
if len(sys.argv) > 1:
    tau = int(sys.argv[1])

t_max = int(math.ceil(5*24*3600/tau))
print "t_max: {}".format(t_max)

start = time.time()
ikt = Slice(data, tau, t_max, start_time)
end = time.time()
print "Slicing took {} s.".format(end - start)


#%% CREATING THE PARTIAL SUMS
start = time.time()
Ikt = CreateSum(ikt)
end = time.time()
print "Creating the partial sums took {} s.".format(end - start)


#%%  
budgets = np.linspace(1, 0.95*n_infections // t_max, 5)
#budget = 10
#budgets = [1]
if len(sys.argv) > 2:
    budgets = [int(i) for i in sys.argv[2:]]
res_optimal = []
res_greedy = []

for r in budgets:
    budget = int(r)
    start = time.time()
    gain_optimal, tab_optimal = OptimalHalting(Ikt, budget)
    end = time.time()
    print "Optimal Halting took {} s for budget {}.".format(end - start, budget)
    print "Optimal had a gain of: {}, for budget {}.".format(gain_optimal, budget)
    print "Optimal had a real gain of: {}, for budget {}.".format(ComputeTotal(tab_optimal, Ikt), budget)
    
    start = time.time()
    gain_greedy, tab_greedy = GreedyHalting(Ikt, budget)
    end = time.time()
    print "Greedy Halting took {} s for budget {}.".format(end - start, budget)
    print "Greedy had a gain of: {}, for budget {}.".format(gain_greedy, budget)
    print "Optimal had a real gain of: {}, for budget {}.".format(ComputeTotal(tab_greedy, Ikt), budget)
    
    res_optimal.append(-gain_optimal)
    res_greedy.append(-gain_greedy)
    
#    print "Optimal res:", res_optimal    
#    print "Greedy res:", res_greedy
#    print "total budget:", [r*t_max*100.0/n_infections for r in budgets[:len(res_greedy)]]

print "Optimal res:", res_optimal    
print "Greedy res:", res_greedy
    

#%% Plot
#res_greedy = [284063, 776626, 1002569]
#res_optimal = [308387.0, 808802.0, 1035433.0]

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

