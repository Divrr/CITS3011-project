from agent import Agent
import random
from itertools import combinations
import math

class Noah(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def normalise_possible_worlds(self):
        total_probability = sum(prob for prob in self.possible_worlds.values())
        for world in self.possible_worlds:
            self.possible_worlds[world] /= total_probability

    def new_game(self, number_of_players, player_number, spies):
        n = number_of_players
        s = super().spy_count[number_of_players]

        self.players = list(range(number_of_players))
        self.spies = spies
        self.spy = True if self.spies else False
        self.id = player_number

        self.possible_worlds = {world: 0 if self.id in world else 1 for world in combinations(self.players, s)}

        self.normalise_possible_worlds()
        
        print("\n".join([f"{world}: {prob}" for world, prob in self.possible_worlds.items()]))

    def propose_mission(self, team_size, betrayals_required):
        return random.sample(self.players, team_size)

    def vote(self, mission, proposer, betrayals_required):
        return True

    def betray(self, mission, proposer, betrayals_required):
        return True

    def vote_outcome(self, mission, proposer, votes):
        pass

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        for world in self.possible_worlds:
            if not mission_success:
                # Discard any world that does not include at least num_betrayals spies in it that were in the mission
                num_spies_on_mission = sum(1 for agent in world if agent in mission)
                if num_spies_on_mission < num_betrayals:
                    self.possible_worlds[world] = 0
            
            self.normalise_possible_worlds()

            # increase suspicion of worlds where the proposer and one member of the 

    def round_outcome(self, rounds_complete, missions_failed):
        print(f"(agent {self.id}) ROUND {rounds_complete} WITH {missions_failed} fails: {"\n".join([f"{world}: {prob}" for world, prob in self.possible_worlds.items()])}")
    
    def game_outcome(self, spies_win, spies):
        pass