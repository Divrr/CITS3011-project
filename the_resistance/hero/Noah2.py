from agent import Agent
import random
from itertools import combinations
import math

class Noah2(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def normalize(self, distribution):
        total = sum(prob for prob in self.possible_worlds.values())
        for d in distribution:
            distribution[d] /= total
        return distribution
    
    def spy_probability(self, spy):
        return sum(prob for world, prob in self.possible_worlds.items() if spy in world)

    def new_game(self, number_of_players, player_number, spies):
        n = number_of_players
        s = super().spy_count[number_of_players]

        self.players = list(range(number_of_players))
        self.spies = spies
        self.spy = True if self.spies else False
        self.id = player_number

        if self.spy:
            self.possible_worlds = {world: 1 for world in combinations(self.players, s)}
        else:
            self.possible_worlds = {world: 1 for world in combinations(self.players, s) if self.id not in world}
        
        self.possible_worlds = self.normalize(self.possible_worlds)

    def propose_mission(self, team_size, betrayals_required):
        top_trusted = sorted([p for p in self.players], key=lambda p: self.spy_probability(p))
        if self.spy:
            spies = [player for player in top_trusted if player in self.spies and player != self.id]
            non_spies = [player for player in top_trusted if player not in self.spies and player != self.id]
            choice = [self.id] + spies[:betrayals_required-1] + non_spies[:team_size - len(spies)+ 1]
        else:
            choice = top_trusted[:team_size]
        
        random.shuffle(choice)
        return choice

    def vote(self, mission, proposer, betrayals_required):
        if self.spy:
            count = sum([1 for teammate in self.spies if teammate in mission])
            return count == betrayals_required
        
        spy_threshold = 0.5
        if self.spy_probability(proposer) > spy_threshold:
            return False
        for member in mission:
            if self.spy_probability(member) > spy_threshold:
                return False
        return True

    def betray(self, mission, proposer, betrayals_required):
        return True

    def vote_outcome(self, mission, proposer, votes):
        pass

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        worlds = self.possible_worlds.copy()
        for world in worlds:
            # assuming this world contains the set of spies, how many were in the mission?
            num_spies_on_mission = sum(1 for agent in world if agent in mission)

            if not mission_success:
                # Discard any world that does not include at least num_betrayals spies in it that were in the mission
                if num_spies_on_mission < num_betrayals:
                    del self.possible_worlds[world]
                    continue

            likelihood = 0
            if mission_success:
                likelihood = 0.1 if num_spies_on_mission else 0.9
            else: 
                likelihood = 0.9 if num_spies_on_mission else 0.1
            
            self.possible_worlds[world] = likelihood * self.possible_worlds[world]

        self.possible_worlds = self.normalize(self.possible_worlds)

    def round_outcome(self, rounds_complete, missions_failed):
        pass

    def game_outcome(self, spies_win, spies):
        pass