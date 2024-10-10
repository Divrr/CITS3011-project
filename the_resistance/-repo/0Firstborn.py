from agent import Agent
import random

class Firstborn(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spies = spies
        self.players = list(range(0, number_of_players))

    def propose_mission(self, team_size, betrayals_required):
        return random.sample(range(0, self.number_of_players), team_size)

    def vote(self, mission, proposer, betrayals_required):
        return True

    def vote_outcome(self, mission, proposer, votes):
        pass

    def betray(self, mission, proposer, betrayals_required):
        return True

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        pass

    def round_outcome(self, rounds_complete, missions_failed):
        pass
    
    def game_outcome(self, spies_win, spies):
        pass