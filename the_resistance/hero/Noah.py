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

    def normalize(self, distribution):
        total = sum(prob for prob in self.possible_worlds.values())
        
        if total == 0:
            return distribution
        
        for d in distribution:
            distribution[d] /= total
        return distribution

    def new_game(self, number_of_players, player_number, spies):
        self.n = number_of_players
        self.s = super().spy_count[self.n]

        self.players = list(range(self.n))
        self.spies = spies

        self.id = player_number
        self.spy = True if self.spies else False

        self.possible_worlds = {world: 1 for world in combinations(self.players, self.s) if self.id not in world}
        
        self.possible_worlds = self.normalize(self.possible_worlds)
        self.trust = {spy: sum(prob for world, prob in self.possible_worlds.items() if spy in world) for spy in self.players}

    def propose_mission(self, team_size, betrayals_required):
        top_trusted = sorted(range(len(self.trust)), key=lambda i: self.trust[i])
        print(self.id, self.trust)
        if self.spy:
            spies = [player for player in top_trusted if player in self.spies]
            non_spies = [player for player in top_trusted if player not in self.spies]
            choice = spies[:betrayals_required] + non_spies[:team_size - betrayals_required]
        else:
            choice = top_trusted[:team_size]
        
        random.shuffle(choice)
        return choice

    def vote(self, mission, proposer, betrayals_required):
        if self.spy:
            count = sum([1 for teammate in self.spies if teammate in mission])
            return count == betrayals_required
        else:
            spy_threshold = 0.5
            if self.trust[proposer] > spy_threshold:
                return False
            for player in mission:
                if self.trust[player] > spy_threshold:
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

            # P(spyA and spyB | fail)
            # = P(spyA|fail)P(spyB|fail)
            # = (P(fail | spyA) P(spyA) / P(fail))(P(fail | spyB) P(spyB) / P(fail))
            # P(fail | spyA) = 0.9
            # P(spA) = previous probability
            # P(fail) = P(fail | spyA)P(spyA) + P(fail | not spyA)P(not spyA)
            # P(fail | not spyA) = 0.1
            # P(not spyA) = 1 - P(spyA)


            p_world_given_outcome = 1
            for member in world:
                if member in mission:
                    if mission_success:
                        p_outcome_given_spy = 0.1
                        p_outcome_given_not_spy = 1
                    else:
                        p_outcome_given_spy = 0.9
                        p_outcome_given_not_spy = 0

                    p_spy = self.trust[member]
                    p_not_spy = 1 - p_spy
                    
                    p_outcome = p_outcome_given_spy * p_spy + p_outcome_given_not_spy * p_not_spy
                    p_spy_given_outcome = p_outcome_given_spy * p_spy / p_outcome

                    p_world_given_outcome *= p_spy_given_outcome

            self.possible_worlds[world] *= p_world_given_outcome
        
        self.possible_worlds = self.normalize(self.possible_worlds)
        self.trust = {spy: sum(prob for world, prob in self.possible_worlds.items() if spy in world) for spy in self.players}

    def round_outcome(self, rounds_complete, missions_failed):
        pass

    def game_outcome(self, spies_win, spies):
        pass