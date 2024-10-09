from agent import Agent
import random

class Adam(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.players = list(range(0, number_of_players))
        self.spies = spies

        self.id = player_number
        self.sus = True if self.spies else False

    def propose_mission(self, team_size, betrayals_required):
        choice = []
        if self.sus:
            choice.extend(random.sample(self.spies, betrayals_required))
        else:
            choice.append(self.id)
        choice.extend(random.sample(self.players, team_size - len(choice)))

        return choice

    def vote(self, mission, proposer, betrayals_required):
        if self.sus:
            count = sum([1 for teammate in self.spies if teammate in mission])
            return count == betrayals_required
        
        return True

    def betray(self, mission, proposer, betrayals_required):
        return True
