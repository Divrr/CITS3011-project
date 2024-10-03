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
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.teammates = spies
        self.players = list(range(0, number_of_players))
        self.players.remove(self.player_number)

        if self.teammates:
            self.is_spy = True
            self.teammates.remove(self.player_number)
        else:
            self.is_spy = False
        
        self.mission = 1
        self.failed_missions = 0


    def propose_mission(self, team_size, betrayals_required):
        choice = [self.player_number]
        if betrayals_required == 2 and self.is_spy:
            choice.append(random.sample(self.teammates, 1))
        choice.extend(random.sample(self.players, team_size-len(choice)))
        return choice

    def vote(self, mission, proposer, betrayals_required):
        if self.is_spy:
            count = 0
            for teammate in self.teammates:
                if teammate in mission:
                    count += 1
            
            if count == betrayals_required:
                return True
            else:
                return False
        
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