from scripts import dynamic_algo
import time
import random
import statistics

def run_trial(players, team_size = 5):
    chosen_players = random.sample(players, TEAM_SIZE * 2)
    players_dict = {}
    for i in range(len(chosen_players)):
        players_dict[i] = chosen_players[i]
    DA = dynamic_algo.DynamicAlgo(players_dict)
    algo_start_time = time.time()
    matchup = DA.matchup()
    algo_end_time = time.time()
    ratings = DA.determine_ratings(matchup)
    margin = DA.calc_margin(ratings)
    runtime = algo_end_time - algo_start_time
    #print(result)
    #print("Time elapsed: ", algo_end_time - algo_start_time)
    return margin, runtime

def run_trials(players, team_size = 5, n = 100):
    margins = []
    runtimes = []
    for i in range(n):
        margin, runtime = run_trial(players, team_size)
        margins.append(margin)
        runtimes.append(runtime)
    print_basic_stats(margins, 'margin')
    print_quantiles(margins, 'margin', 100)
    print_basic_stats(runtimes, 'runtime')

def print_basic_stats(data, label):
    print("Trials: ", len(data))
    print("Lowest {}: ".format(label), min(data))
    print("Median {}: ".format(label), statistics.median(data))
    print("Average {}: ".format(label), statistics.mean(data))
    print("Highest {}: ".format(label), max(data))

def print_quantiles(data, label, n = 4):
    # we don't really know that it's inclusive but i prefer it
    print("Quantiles for", label)
    quants = statistics.quantiles(data=data, n=n, method='inclusive')
    for i in range(n - 1):
        print((i+1) / n, '=', quants[i])

if __name__=="__main__":
    TEAM_SIZE = 5
    players_lst = []
    with open("test_dynamic.csv") as f:
        for line in f:
            line = line.strip('\n').split(',')
            # lil hardcoded here eh
            ind = 0
            while ind < len(line):
                try:
                    line[ind] = int(line[ind])
                except:
                    pass
                ind += 1
            players_lst.append(line)
    run_trials(players_lst, 5, 5000)
