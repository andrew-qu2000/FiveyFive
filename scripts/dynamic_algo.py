"""
dynamic_algo
"""
from copy import deepcopy

class DynamicAlgo():
    """
    Class for algorithmic approach to selecting the best team matchup.

    Attributes:
        squad    (dict): a dictionary of Players with keys as UUID
        team_size (int): index that divides the squad into two teams
        explored (dict): a dictionary of explored states, values are None
    """
    def __init__(self, squad):
        self.squad = squad
        self.team_size = int(len(squad) / 2)
        self.explored = {}

    def matchup(self):
        """
        Main method for determining the best matchup from a squad

        Given: squad of 10 players with 5 ratings each
        Return: two subsets of 5 players where the average of each 
                subset yields the smallest margin

        This is a variation of the Simulated Annealing technique. The algorithm 
        derives possible states from a starting matchup by performing single 
        player swaps and deriving the subsequent state's margin.

        The current state of the algorithm only returns a local minimum margin.
        By fully implementing the Simulated Annealing technique, a global 
        minimum can be achieved.
        """
        # select a starting matchup (easiest is the initial squad itself)
        matchup = list(self.squad.keys())
        # determine the ratings for the current matchup
        ratings = self.determine_ratings(matchup)
        # calculate the margin of the matchup
        margin = self.calc_margin(ratings)
        # get next states and their margins
        states = self.next_states(matchup)
        for state in states:
            ratings = self.determine_ratings(state)
            print("==========")
            print(state)
            margin = self.calc_margin(ratings)

        pass

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
        print("teams:", team_r, "|", team_b, " margin:", margin)
        return margin

    def determine_ratings(self, matchup):
        """
        Determing the ratings for each player according to positions
        
        Takes a list of Player UUIDs that represents a matchup.
        Returns a list of tuples of (Player UUID, rating).
        """
        rated = []
        for idx, player in enumerate(matchup):
            # grab the correct rating according to the pos on team
            # accounts for the first element being the name of the player
            rated.append((player, self.squad[player][1 + idx % self.team_size]))
        return rated

    def next_states(self, matchup):
        """
        Perform single-swaps between players to get the next matchups

        Disregard duplicate states by not performing the same swaps
        """
        states = []
        match_size = int(len(matchup)) - 1
        for x in range(match_size):
            for y in range(x, match_size):
                # we do not want to mutate the original matchup
                temp = deepcopy(matchup)
                # perform a single swap and add to list of states
                temp[x], temp[y+1] = temp[y+1], temp[x]
                # check if the state has already been explored
                if temp in self.explored.keys():
                    continue
                else: # else, add to list of states and to the explored dict
                    states.append(temp)
                    self.explored[temp] = None
        return states


a, b, c, d = ["A", 68, 66], ["B", 82, 75], ["C", 92, 93], ["D", 72, 84]
squad = {135:a, 246:b, 357:c, 468:d}
matchup = list(squad.keys())

da = DynamicAlgo(squad)
da.matchup()