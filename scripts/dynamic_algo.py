"""
dynamic_algo
"""
from copy import deepcopy

class DynamicAlgo():
    """
    Class for algorithmic approach to selecting the best team matchup.

    Attributes:
        squad    (dict): a dictionary of Players with keys as UUIDs
        team_size (int): index that divides the squad into two teams
        explored  (set): a set of explored states, initialized empty
    """
    def __init__(self, squad):
        self.squad = squad
        self.team_size = int(len(squad) / 2)
        self.explored = set()
        self.rating_names = ['rating_top', 'rating_jun', 'rating_mid', 'rating_bot', 'rating_sup']


    def matchup(self):
        """
        Main method for determining the best matchup from a squad

        Given: squad of N players with N/2 ratings each
        Return: a matchup of N players where the average of each 
                team yields the smallest margin

        This is a variation of the Simulated Annealing technique. The algorithm 
        derives possible states from a starting matchup by performing single 
        player swaps and deriving the subsequent state's margin.

        The current state of the algorithm only returns a local minimum margin.
        By fully implementing the Simulated Annealing technique, a global 
        minimum can be achieved.
        """
        margins = [] # list for keeping track of an iteration's margins
        # select a starting matchup (easiest is the initial squad itself)
        curr_matchup = list(self.squad.keys())
        
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
        for idx, player in enumerate(matchup):
            # grab the correct rating according to the pos on team
            # accounts for the first element being the name of the player
            rating_ind = idx % self.team_size
            rating_name = self.rating_names[rating_ind]
            rated.append((player, self.squad[player][rating_name]))
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
    
    a, b, c = ["ay", 51, 94, 83], ["be", 97, 73, 79], ["si", 66, 91, 74]
    d, e, f = ["di", 86, 85, 52], ["ee", 77, 99, 96], ["ef", 70, 54, 72]
    squad = {'A':a, 'B':b, 'C':c, 'D':d, 'E':e, 'F':f}
    
    da = DynamicAlgo(squad)
    print(da.matchup())