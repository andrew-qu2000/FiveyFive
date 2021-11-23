"""
brute_algo
"""

from itertools import permutations


class BruteAlgo():
    """
    Class for brute force approach to selecting the best team matchup.

    Attributes:
        squad (dict): dictionary of Players with keys as UUIDs
    """

    def __init__(self, squad):
        self.squad = squad
        self.team_size = int(len(squad) / 2)
        pass

    def matchup(self):
        """
        Main method for determining the best matchup from a squad

        Given: squad of N players with N/2 ratings each
        Return: a matchup of N players where the average of each 
                team yields the smallest margin

        This approach guarantees that the global best matchup is selected.
        However, the runtime of the algorithm does increase as the size of 
        the teams increases. This is not ideal when trying to serve a best
        matchup to a client in a timely manner.
        """
        margins = set()
        keys = list(self.squad.keys())
        
        # loop through all possible variations of the matchup
        for matchup in permutations(keys):
            ratings = self.determine_ratings(matchup)
            margins.add((self.calc_margin(ratings), matchup))

        # determine which states have the smallest margin
        min_margin = min(margins)[0]
        min_states = [s for _, s in enumerate(margins) if s[0] == min_margin]

        state = min_states.pop()
        print("best matchup:", state[0], "|", state[1])

        # return one min state
        return state[1]

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
            rating_ind = (idx % self.team_size) + 1
            rated.append((player, self.squad[player][rating_ind]))
        return rated


if __name__ == "__main__":
    #a, b, c, d = ["ay", 68, 66], ["be", 82, 75], ["si", 92, 93], ["di", 72, 84]
    #squad = {'A':a, 'B':b, 'C':c, 'D':d}

    a, b, c = ["ay", 51, 94, 83], ["be", 97, 73, 79], ["si", 66, 91, 74]
    d, e, f = ["di", 86, 85, 52], ["ee", 77, 99, 96], ["ef", 70, 54, 72]
    squad = {'A':a, 'B':b, 'C':c, 'D':d, 'E':e, 'F':f}

    ba = BruteAlgo(squad)
    print(ba.matchup())