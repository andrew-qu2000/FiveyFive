"""
This is the test suite for dynamic_algo.py
"""

from unittest import TestCase

from scripts.dynamic_algo import DynamicAlgo

# sample data
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
team_size = int(len(squad)/2)
rating_names = ['rating_top', 'rating_jun', 'rating_mid', 'rating_bot', 'rating_sup']

DA = DynamicAlgo(squad, rating_names)

class DynamicTestCase(TestCase):

    def test_class_attributes(self):
        """
        Make sure the attributes are as expected

        squad: the squad itself (should be the same length as input)
        team_size: should be half the size of the squad
        explored: should be an empty set
        rating_names: should be
            ['rating_top', 'rating_jun', 'rating_mid', 'rating_bot', 'rating_sup']
        """
        self.assertEqual(DA.squad, squad)
        self.assertEqual(DA.team_size, team_size)
        self.assertFalse(DA.explored)
        self.assertEqual(DA.rating_names, rating_names)

    def test_determine_ratings_length(self):
        """
        Ensure equal input and output lengths
        """
        initial_len = len(DA.squad)
        final_len = len(DA.determine_ratings(DA.squad.keys()))

        self.assertEqual(initial_len, final_len)

    def test_determine_ratings(self):
        """
        Make sure that the ratings of the players matches the players
        """
        list_of_players = list(DA.squad.keys())
        list_of_ratings = []
        for ind, player in enumerate(list_of_players):
            rating_ind = ind % team_size
            rating_pos = rating_names[rating_ind]
            list_of_ratings.append((player, squad[player][rating_pos]))
        DAratings = DA.determine_ratings(list_of_players)

        self.assertEqual(DAratings, list_of_ratings)

    def test_calc_margin(self):
        """
        Make sure that the margin calculation is >= 0
        """
        matchup = list(DA.squad.keys())
        ratings = DA.determine_ratings(matchup)
        margin = DA.calc_margin(ratings)
        self.assertGreaterEqual(margin, 0)

    # def test_fail_on_purpose(self):
    #     """
    #     Fail and see if this prevents automatic deployment to Heroku through Github Actions
    #     """
    #     self.assertEqual(0,1)
