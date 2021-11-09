# In-house team building
# Complete Search (brute force)
# Positional ratings

import numpy as np
import pandas as pd
import time
from itertools import combinations, permutations
import random
import json

start_time = time.time()

f = open("game_settings.json")
settings = json.load(f)
f.close()
NUM_PLAYERS = settings['num-players']
TEAM_SIZE = NUM_PLAYERS / 2
TEAM_NAME = settings['team-names']
POSITIONS = settings['positions']
WEIGHTS = settings['weights']

players = pd.read_csv("inhouse_positional.csv")
players = players[players['Playing']]
assert(players.shape[0] == NUM_PLAYERS)
# Top, Jun, Mid, Bot, Sup -> 3, 4, 5, 6, 7
players_mat = players.to_numpy()
onrole_ratings = [max(row[3:8]) for row in players_mat]


def calc_team(team_idx):
    total_rating = 0
    total_offrole = 0
    for i in range(len(team_idx)):
        player_idx = team_idx[i]
        assigned_rating = players_mat[player_idx][i+3]
        total_rating += assigned_rating * WEIGHTS[i]
        total_offrole += onrole_ratings[player_idx] - assigned_rating
    return total_rating / TEAM_SIZE , total_offrole

def calc_matchup_score(matchup):
    # score = (team diff) * 2 + (team one offrole) + (team two offrole)
    # lower score ~ better game
    team_one = matchup[:TEAM_SIZE]
    team_two = matchup[TEAM_SIZE:]
    rating_one, offrole_one = calc_team(team_one)
    rating_two, offrole_two = calc_team(team_two)
    #return abs(rating_one - rating_two) * 2 + offrole_one + offrole_two
    return abs(rating_one - rating_two)
    
def print_team(team_idx, team_name):
    print(team_name)
    for i in range(len(team_idx)):
        player = players_mat[team_idx[i]]
        print(POSITIONS[i], player[0], player[i+3])
    team_score = calc_team(team_idx)
    print("Team average = {0:.2f}".format(team_score[0]))
    print("Team offroleness =", team_score[1])
    print("=" * 20)

def print_matchup(matchup):
    print_team(matchup[:TEAM_SIZE], TEAM_NAME[0])
    print_team(matchup[TEAM_SIZE:], TEAM_NAME[1])
    
# Find 5 closest matches
# TODO: Every matchup appears twice (only diff is order of teams)
#       Can halve runtime by only going through first half

def main():
    best_matchups = []
    best_matchups_scores = []

    #perms_done = 0

    perm_lst = [0,1,2,3,4,5,6,7,8,9]
    random.shuffle(perm_lst)

    for matchup in permutations(perm_lst):
        mu_score = calc_matchup_score(matchup)
        if len(best_matchups) == 10:
            if mu_score < best_matchups_scores[9]:
                score_idx = 0
                while mu_score > best_matchups_scores[score_idx]:
                    score_idx += 1
                best_matchups.insert(score_idx, matchup)
                best_matchups.pop()
                best_matchups_scores.insert(score_idx, mu_score)
                best_matchups_scores.pop()
        else:
            best_matchups.append(matchup)
            best_matchups_scores.append(mu_score)
        #perms_done += 1
        #if perms_done % 100000 == 0:
        #    print(perms_done)

    end_time = time.time()
    print(f"Matchup found in {end_time - start_time} seconds")

    for matchup in best_matchups:
        print_matchup(matchup)

if __name__ == "__main__":
    main()