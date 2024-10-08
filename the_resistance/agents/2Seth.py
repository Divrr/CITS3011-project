from agent import Agent
import random

class Seth(Agent):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        self.players = list(range(0, number_of_players))
        self.spies = spies
        self.trust = [1] * number_of_players

        self.id = player_number
        self.spy = True if self.spies else False

        self.votes = []

    def propose_mission(self, team_size, betrayals_required):
        choice = []
        if self.spy:
            pool = self.players.copy()
            random.shuffle(pool)
            
            spies = [player for player in pool if player in self.spies and player != self.id]
            non_spies = [player for player in pool if player not in self.spies and player != self.id]

            choice = [self.id] + spies[:betrayals_required-1] + non_spies[:team_size - len(spies)+ 1]
        else:
            priority = sorted([(i, score) for i, score in enumerate(self.trust)], key=lambda x: -x[1])
            top = [i for i, score in priority[:team_size]]
            choice.extend(top)
        
        random.shuffle(choice)
        return choice

    def vote(self, mission, proposer, betrayals_required):
        if self.spy:
            count = sum([1 for teammate in self.spies if teammate in mission])
            return count == betrayals_required
        else:
            if self.trust[proposer]<=0.1:
                return False
            for player in mission:
                if self.trust[player] <= 0.1:
                    return False
            return True

    def betray(self, mission, proposer, betrayals_required):
        return True

    def vote_outcome(self, mission, proposer, votes):
        self.votes = votes

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        if not mission_success:
            self.trust[proposer] /= len(mission)
            for player in mission:
                self.trust[player] /= len(mission)
            for voter in self.votes:
                self.trust[voter] /= len(mission)
        self.trust[self.id] = 1

    def round_outcome(self, rounds_complete, missions_failed):
        pass
    
    def game_outcome(self, spies_win, spies):
        pass