"""
This is a variation of the Simulated Annealing technique. The algorithm
derives possible states from a starting matchup by performing single
player swaps and deriving the subsequent state's margin.

The current state of the algorithm only returns a local minimum margin.
By fully implementing the Simulated Annealing technique, a global
minimum can be achieved.
"""
from copy import deepcopy
import random

class DynamicAlgo():
    """
    Class for algorithmic approach to selecting the best team matchup.

    Attributes:
        squad    (dict): a dictionary of Players with keys as UUIDs
        team_size (int): index that divides the squad into two teams
        explored  (set): a set of explored states, initialized empty
    """
    def __init__(self, squad, positions, weights):
        self.squad = squad
        self.team_size = int(len(squad) / 2)
        self.explored = set()
        self.rating_names = positions
        self.rating_weights = weights


    def matchup(self, random_initial):
        """
        Main method for determining the best matchup from a squad

        Given: squad of N players with N/2 ratings each
        Return: a matchup of N players where the average of each
                team yields the smallest margin
        """
        margins = [] # list for keeping track of an iteration's margins
        # select a starting matchup (easiest is the initial squad itself)
        curr_matchup = list(self.squad.keys())
        #print(curr_matchup)
        if (random_initial):
            #print('shuffling')
            random.shuffle(curr_matchup)
        while curr_matchup:
            # determine the ratings and calculate margin for the matchup
            curr_ratings = self.determine_ratings(curr_matchup)
            margins.append((self.calc_margin(curr_ratings), curr_matchup))

            # get next states and their margins
            states = self.get_states(curr_matchup)

            for state in states:
                ratings = self.determine_ratings(state)
                margins.append((self.calc_margin(ratings), state))

            # get states with smallest margin and reset margins list
            min_margin = min(margins)[0]
            min_states = [s[1] for _, s in enumerate(margins) if s[0] == min_margin]
            margins = []

            if curr_matchup in min_states: # best matchup has been found
                #print(min_margin)
                return curr_matchup
            else:
                next_state = min_states.pop()
                if min_margin:
                    # get the next state with the lowest margin
                    # if there are more than one state in min_states,
                    # a local best matchup is found.
                    curr_matchup = next_state
                else:
                # the next state has a margin of 0, best matchup has been found
                    return next_state

    def calc_margin(self, ratings):
        """
        Method for calculating the margin between two teams in a matchup

        The first half of the matchup is considered the first team
        and the latter half is the second team. The margin is calculated
        by adding all of the ratings in each team and finding the
        absolute difference between the teams.
        """
        team_r = ratings[:self.team_size]
        team_b = ratings[self.team_size:]
        margin = abs(sum(r for _, r in team_r) - sum(r for _, r in team_b))
        #print("teams:", team_r, "|", team_b, " margin:", margin)
        return margin

    def determine_ratings(self, matchup):
        """
        Determing the ratings for each player according to positions

        Takes a list of Player UUIDs that represents a matchup.
        Returns a list of tuples of (Player UUID, rating).
        """
        rated = []
        # TODO: reflect change to generalized position labels instead of indices
        for idx, player in enumerate(matchup):
            # grab the correct rating according to the pos on team
            # accounts for the first element being the name of the player
            rating_ind = idx % self.team_size
            rating_name = self.rating_names[rating_ind]
            rating_weight = self.rating_weights[rating_ind]
            rated.append((player, self.squad[player][rating_name] * rating_weight))
        return rated

    def get_states(self, matchup):
        """
        Perform single-swaps between players to get the next matchups

        Disregard duplicate states by not performing the same swaps.
        Also disregard if the state has been explored already.
        """
        states = []
        match_size = int(len(matchup)) - 1
        for x in range(match_size):
            for y in range(x, match_size):
                # we do not want to mutate the original matchup
                temp = deepcopy(matchup)
                # perform a single swap and add to list of states
                temp[x], temp[y+1] = temp[y+1], temp[x]
                # add to list of states and to the explored dict
                states.append(temp)
                self.explored.add(tuple(temp)) # a set will not add dupes
        return states

if __name__ == "__main__":
    #a, b, c, d = ["ay", 68, 66], ["be", 82, 75], ["si", 92, 93], ["di", 72, 84]
    #squad = {'A':a, 'B':b, 'C':c, 'D':d}

    a = {'rating_top': 69, 'rating_mid': 77, 'name': 'Terence', 'rating_bot': 68, 'rating_sup': 60, 'rating_jun': 66}
    b = {'rating_top': 75, 'rating_bot': 75, 'name': 'Jordon', 'rating_mid': 75, 'rating_jun': 75, 'rating_sup': 75}
    c = {'rating_top': 65, 'rating_mid': 65, 'rating_jun': 75, 'rating_sup': 83, 'name': 'Aymen', 'rating_bot': 82}
    d = {'rating_jun': 93, 'rating_top': 88, 'rating_bot': 96, 'rating_sup': 91, 'rating_mid': 89, 'name': 'Sean'}
    e = {'rating_top': 60, 'name': 'Cameron', 'rating_bot': 69, 'rating_sup': 55, 'rating_jun': 62, 'rating_mid': 60}
    f = {'rating_bot': 72, 'rating_jun': 94, 'rating_mid': 80, 'name': 'Nick', 'rating_sup': 85, 'rating_top': 78}
    g = {'name': 'Gavin', 'rating_mid': 83, 'rating_jun': 85, 'rating_top': 84, 'rating_sup': 85, 'rating_bot': 82}
    h = {'rating_sup': 71, 'rating_mid': 73, 'name': 'Matthew', 'rating_top': 83, 'rating_bot': 65, 'rating_jun': 80}
    i = {'rating_sup': 86, 'name': 'Andrew', 'rating_bot': 85, 'rating_jun': 85, 'rating_top': 92, 'rating_mid': 86}
    j = {'rating_top': 70, 'name': 'Alex', 'rating_mid': 70, 'rating_jun': 69, 'rating_sup': 68, 'rating_bot': 62}
    squad = {'A':a, 'B':b, 'C':c, 'D':d, 'E':e, 'F':f, 'G':g, 'H':h, 'I':i, 'J':j}

    da = DynamicAlgo(squad)
    print(da.matchup())
