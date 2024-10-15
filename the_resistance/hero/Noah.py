from agent import Agent
import random
from itertools import combinations
import math

SPY_THRESHOLD = 0.5
P_MISSION_FAIL_GIVEN_SPY = 0.7 # spies usually fail missions
P_MISSION_SUCCESS_GIVEN_SPY = 0.3 # spies don't usually succeed missions
P_MISSION_FAIL_GIVEN_RES = 0 # resistance can't fail missions
P_MISSION_SUCCESS_GIVEN_RES = 1 # resistance always succeeds missions

class Noah(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def normalize(self, distribution):
        total = sum(prob for prob in distribution.values())
        
        if total == 0:
            return distribution
        
        for d in distribution:
            distribution[d] /= total
        return distribution

    def update_trust(self):
        trust_counts = {player: 0 for player in self.players}
        for world, prob in self.possible_worlds.items():
            for player in world:
                trust_counts[player] += prob
        self.trust = trust_counts

    def new_game(self, number_of_players, player_number, spies):
        self.n = number_of_players
        self.s = super().spy_count[self.n]

        self.players = list(range(self.n))
        self.spies = spies

        self.id = player_number
        self.spy = True if self.spies else False

        self.possible_worlds = {world: 1 for world in combinations(self.players, self.s) if self.id not in world}
        
        self.possible_worlds = self.normalize(self.possible_worlds)
        self.update_trust()

        self.round_no = 1
        self.missions_failed = 0

    def propose_mission(self, team_size, betrayals_required):
        top_trusted = sorted(self.trust.keys(), key=lambda player: (self.trust[player], random.random()))
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
            if self.trust[proposer] > SPY_THRESHOLD:
                return False
            for player in mission:
                if self.trust[player] > SPY_THRESHOLD:
                    return False
            return True

    def betray(self, mission, proposer, betrayals_required):
        if self.missions_failed >= 2:
            return True
        if self.round_no == 4:
            return True
        
        num_spies_on_mission = sum(1 for agent in mission if agent in self.spies)
        if num_spies_on_mission > betrayals_required:
            return random.random() < 0.3
        elif num_spies_on_mission == betrayals_required and len(mission) >= betrayals_required:
            return True
        else:
            return False
        
        return True

    def vote_outcome(self, mission, proposer, votes):
        pass

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        def calculate_p_spy_given_outcome(p_outcome_given_spy, p_outcome_given_res, p_spy, p_res):
            p_outcome = p_outcome_given_spy * p_spy + p_outcome_given_res * p_res
            return p_outcome_given_spy * p_spy / p_outcome
        
        worlds_to_delete = []
        for world in self.possible_worlds:
            # Discard any world that does not include at least num_betrayals spies in it that were in the mission
            if not mission_success:
                num_spies_on_mission = sum(1 for agent in world if agent in mission)
                if num_spies_on_mission < num_betrayals:
                    worlds_to_delete.append(world)
                    continue

            p_world_given_outcome = 1
            for member in mission:
                if member in world:
                    p_spy_given_outcome = calculate_p_spy_given_outcome(
                        P_MISSION_SUCCESS_GIVEN_SPY if mission_success else P_MISSION_FAIL_GIVEN_SPY,
                        P_MISSION_SUCCESS_GIVEN_RES if mission_success else P_MISSION_FAIL_GIVEN_RES,
                        self.trust[member],
                        1 - self.trust[member]
                    )
                    p_world_given_outcome *= p_spy_given_outcome

            self.possible_worlds[world] *= p_world_given_outcome

        for world in worlds_to_delete:
            del self.possible_worlds[world]
        
        self.possible_worlds = self.normalize(self.possible_worlds)
        self.update_trust()

    def round_outcome(self, rounds_complete, missions_failed):
        self.round_no = rounds_complete
        self.missions_failed = missions_failed

    def game_outcome(self, spies_win, spies):
        pass
