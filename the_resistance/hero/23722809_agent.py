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
        self.players = list(range(number_of_players))
        self.spies = spies
        self.trust = [1] * number_of_players

        self.id = player_number
        self.spy = True if self.spies else False

        self.votes = []
        self.round_no = 1
        self.missions_failed = 0

    def propose_mission(self, team_size, betrayals_required):
        # Pick the most trusted players, tiebreaking randomly. See report for more details on reasoning.
        top_trusted = sorted(range(len(self.trust)), key=lambda i: (-self.trust[i], random.random()))
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
            if self.trust[proposer]<=0.1:
                return False
            for player in mission:
                if self.trust[player] <= 0.1:
                    return False
            return True

    def betray(self, mission, proposer, betrayals_required):
        return True

    def vote_outcome(self, mission, proposer, votes):
        # Did I vote for the mission?
        voted = self.vote(
            mission, 
            proposer, 
            super().betrayals_required[len(self.players)][self.round_no]
        )

        # Get suspicious of players who voted differently to me
        for player in self.players:
            player_voted = player in votes
            if voted != player_voted:
                self.trust[player] /= 2
        
        self.votes = votes

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        # Get suspicious of players who were...
        # - on the mission
        # - proposer
        # - voted for the mission

        if not mission_success:
            self.trust[proposer] /= len(mission)
            for player in mission:
                self.trust[player] /= len(mission)
            for voter in self.votes:
                self.trust[voter] /= len(mission)
        self.trust[self.id] = 1

    def round_outcome(self, rounds_complete, missions_failed):
        self.round_no = rounds_complete
        self.missions_failed = missions_failed
    
    def game_outcome(self, spies_win, spies):
        pass