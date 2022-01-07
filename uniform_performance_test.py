from scripts import dynamic_algo
import numpy as np
import pandas as pd
import time
import random
import statistics

def run_trial(players, team_size = 5):
    """Performs the dynamic algorithm and returns metrics.

    Forms two random initial teams out of the given players.
    Uses the dynamic algorithm to find a close matchup.
    Returns skill margin between teams and runtime of the algorithm.

    Positional arguments:
    players (DataFrame): DataFrame of players represented as [pos1, pos2, ..., posN, name]

    Keyword arguments:
    team_size (int): number of players on each team
    """

    chosen_players_df = players.sample(TEAM_SIZE * 2)
    players_dict = chosen_players_df.to_dict('index')
    DA = dynamic_algo.DynamicAlgo(players_dict, chosen_players_df.columns)
    algo_start_time = time.time()
    matchup = DA.matchup(False)
    algo_end_time = time.time()
    ratings = DA.determine_ratings(matchup)
    margin = DA.calc_margin(ratings)
    runtime = algo_end_time - algo_start_time
    return margin, runtime

def run_trials(players, team_size = 5, n = 100):
    """Performs many trials of the dynamic algorithm.

    Repeatedly calls run_trial and stores the results.
    Prints statistics on performance metrics.

    Positional arguments:
    players (DataFrame) -- players to pass to run_trial()

    Keyword arguments:
    team_size (int) -- number of players on each team
    n (int) -- number of trials to perform
    """
    margins = []
    runtimes = []
    for i in range(n):
        margin, runtime = run_trial(players, team_size)
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

def generate_ratings(position_labels, dist = 'uniform', n_players = 15, low = 50, high = 100, center = 75, stdev = 10):
    names = []
    with open('names.txt', 'r') as f:
        for line in f:
            names.append(line.strip())

    names = pd.Series(random.sample(names, n_players))
    rng = np.random.default_rng()
    if dist == 'uniform':
        data = rng.integers(low, high, (n_players, len(position_labels)))
    elif dist == 'normal':
        # numpy.random.Generator is the practice now
        # but the normal distribution returns floats
        # so I guess I'll just round them
        data = rng.normal(center, stdev, (n_players, len(position_labels))).round().astype(int)
    elif dist == 'one_main':
        # In real life, most players main one position,
        # Which should have a better rating than the other positions
        data = np.empty((0,len(position_labels)), dtype=int)
        for i in range(n_players):
            offrole_center = rng.uniform(center - stdev * 1.5, center + stdev)
            offrole_ratings = rng.normal(offrole_center, stdev / 2, len(position_labels) - 1).round().astype(int)
            mainrole_rating = rng.integers(offrole_ratings.max() + stdev // 2, offrole_ratings.max() + stdev * 2)
            ratings = np.insert(offrole_ratings, rng.integers(0,len(position_labels)), mainrole_rating)
            data = np.append(data, [ratings], axis = 0)
    df = pd.DataFrame(data, columns = position_labels)
    df['name'] = names
    print(df)
    return df

if __name__=="__main__":
    TEAM_SIZE = 5
    players_lst = []
    positions = ['rating_top', 'rating_jun', 'rating_mid', 'rating_bot', 'rating_sup']

    #run_trials(generate_ratings(positions, n_players = 30, low = 70, high = 100), team_size = 5, n = 1000)
    run_trials(generate_ratings(positions, dist = 'normal'), team_size = 5, n = 100)
    run_trials(generate_ratings(positions, dist = 'one_main'), team_size = 5, n = 100)
