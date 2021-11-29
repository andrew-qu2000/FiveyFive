from scripts import dynamic_algo
import time
import random
import statistics

def run_trial(players, rating_names, team_size = 5):
    """Performs the dynamic algorithm and returns metrics.

    Forms two random initial teams out of the given players.
    Uses the dynamic algorithm to find a close matchup.
    Returns skill margin between teams and runtime of the algorithm.

    Positional arguments:
    players (list): 2D list of players represented as [name, pos1, pos2 ...]
    rating_names (list): list of positional names to be used as keys (top, jun, mid ...)
    
    Keyword arguments:
    team_size (int): number of players on each team
    """
    chosen_players = random.sample(players, TEAM_SIZE * 2)
    players_dict = {}
    for player_idx in range(len(chosen_players)):
        single_dict = {'name':chosen_players[player_idx][0]}
        for pos_idx in range(len(rating_names)):
            single_dict[rating_names[pos_idx]] = chosen_players[player_idx][pos_idx+1]
        players_dict[player_idx] = single_dict
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

def run_trials(players, rating_names, team_size = 5, n = 100):
    """Performs many trials of the dynamic algorithm.

    Repeatedly calls run_trial and stores the results.
    Prints statistics on performance metrics.

    Positional arguments:
    players (list) -- players to pass to run_trial()

    Keyword arguments:
    team_size (int) -- number of players on each team
    n (int) -- number of trials to perform
    """
    margins = []
    runtimes = []
    for i in range(n):
        margin, runtime = run_trial(players, rating_names, team_size)
        margins.append(margin)
        runtimes.append(runtime)
    print_basic_stats(margins, 'margin')
    print_quantiles(margins, 'margin', 100)
    print_basic_stats(runtimes, 'runtime')
    print_quantiles(runtimes, 'runtime', 100)
    
def print_basic_stats(data, label):
    """Prints statistics on a set of numeric data.

    Calculates and prints the minimum, median, mean, and maximum of a list of
    numbers.

    Positional arguments:
    data (iterable): iterable container of numbers
    label (str): name of this dataset
    """
    print("Trials: ", len(data))
    print("Lowest {}: ".format(label), min(data))
    print("Median {}: ".format(label), statistics.median(data))
    print("Average {}: ".format(label), statistics.mean(data))
    print("Highest {}: ".format(label), max(data))

def print_quantiles(data, label, n = 4):
    """Prints quantiles of a set of numeric data.

    Calculates and prints quantile thresholds.

    Positional arguments:
    data (iterable): iterable container of numbers
    label (str): name of this dataset

    Keyword arguments:
    n (int): number of quantiles to create
    """
    # we don't really know that it's inclusive but i prefer it
    print("Quantiles for", label)
    quants = statistics.quantiles(data=data, n=n, method='inclusive')
    for i in range(n - 1):
        print((i+1) / n, '=', quants[i])

if __name__=="__main__":
    TEAM_SIZE = 5
    players_lst = []
    positions = ['rating_top', 'rating_jun', 'rating_mid', 'rating_bot', 'rating_sup']
    with open("performance_test.csv") as f:
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
    run_trials(players_lst, positions, 5, 1000)
