from agent import Agent
import random
from itertools import combinations

class Noah(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.number_of_players = number_of_players
        self.number_of_spies = super().spy_count[number_of_players]

        self.players = list(range(number_of_players))
        self.spies = spies
        self.spy = True if self.spies else False
        self.id = player_number

        if self.spy:print(spies)
        self.possible_worlds = {
            player:{
                world: 0 if player in world else 1
                    for world in combinations(self.players, self.number_of_spies)
            } for player in self.players
        }

        self.aggregate_trust = {player: 0 for player in self.players}
        for player in self.possible_worlds:
            for world in self.possible_worlds[player]:
                for agent in world:
                    self.aggregate_trust[agent] += self.possible_worlds[player][world]

    def propose_mission(self, team_size, betrayals_required):
        trust_buckets = {i: [] for i in self.aggregate_trust.values()}
        for player, trust in self.aggregate_trust.items():
            trust_buckets[trust].append(player)
        
        trust_buckets = sorted(trust_buckets.items())

        choice = []

        for trust, players in trust_buckets:
            random.shuffle(players)

            for player in players:
                if len(choice) == team_size: break
                choice.append(player)
        
        print(trust_buckets)
        return choice

    def vote(self, mission, proposer, betrayals_required):
        return True

    def betray(self, mission, proposer, betrayals_required):
        return True

    def vote_outcome(self, mission, proposer, votes):
        pass

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        if mission_success:
            print(f"\033[92m", end="")
        else:
            print(f"\033[91m", end="")
        print(mission)
        
        for player in self.players:
            if not mission_success:
                # Reduce any combination that does not include at least num_betrayals spies in the subset down to 0
                for world in self.possible_worlds[player]:
                    # if the subset WAS spies, how many got into the mission?
                    num_spies_on_mission = sum(1 for agent in world if agent in mission)
                    # if the numbers don't add up, that world is not correct
                    if num_spies_on_mission < num_betrayals:
                        self.possible_worlds[player][world] = 0
        
        self.aggregate_trust = {player: 0 for player in self.players}
        for player in self.possible_worlds:
            for world in self.possible_worlds[player]:
                for agent in world:
                    self.aggregate_trust[agent] += self.possible_worlds[player][world]
        
        print(self.aggregate_trust)

    def round_outcome(self, rounds_complete, missions_failed):
        print(f"======={rounds_complete, missions_failed}=======")
    
    def game_outcome(self, spies_win, spies):
        pass