from agent import Agent
import random
from statistics import stdev

# Important: Make sure you put your agents in the agents folder, so that the
# game runner code can find them.

class V2BayesAgent(Agent):        
    '''A sample implementation of a random agent in the game The Resistance'''

    def __init__(self, name = 'Test'):
        '''
        Initialises the agent.
        '''
        self.name = name

    def new_game(self, number_of_players, player_number, spy_list):
        '''
        initialises the game, informing the agent of the 
        number_of_players, the player_number (an id number for the agent in the game),
        and a list of agent indexes which are the spies, if the agent is a spy, or empty otherwise
        '''
        self.number_of_players = number_of_players
        self.all_players = list(range(number_of_players))
        self.other_players = [pn for pn in self.all_players if pn != player_number]
        self.me = player_number
        self.spy_list = spy_list
        self.number_of_spies = self.spy_count[number_of_players]
        # assign an inital "suspicison" of being a spy
        # my agent will treat every player equally, even if it knows someone is a spy, it will still assign suspicison scores to them
        self.suspicion_of_being_spy = {pn:  self.number_of_spies/(number_of_players-1) for pn in range(number_of_players) if pn != player_number}
        self.total_average_suspicion = self.number_of_spies/(number_of_players-1)
        #self.all_votes = {i:set() for i in range(1,6)}
        self.latest_set_of_votes = set()
        self.upcoming_mission_number = 1
        self.number_of_wins = 0 # this will be wins for either spy or resistance member
        self.high_chance_spy = set()
        self.wins_per_player = {pn: 0 for pn in range(number_of_players) if pn != player_number} 
        self.all_votes = {p: {'incorrect_votes': 0, 'correct_votes': 0} for p in range(number_of_players) if p != player_number}
        #self.proposer_votes = {p:  for p in range(number_of_players) if p != player_number}
        self.failing_mission_teams = []
        self.failing_votes_teams = [] # this will be a list of sets of players who voted wrong
        self.vote_sus_scaling = {1: 0.3, 2: 0.5, 3: 0.65, 4: 0.8, 5: 0.85}
        self.decrease_suspicion_scaling = {1: 0.95, 2: 0.9, 3: 0.7, 4: 0.5, 5: 0.45}
        self.number_res_wins = 0
        self.number_spy_wins = 0
        self.proposer_track_record = {p: 0 for p in range(number_of_players) if p != player_number}


    def is_spy(self):
        '''
        returns True iff the agent is a spy
        '''
        return self.me in self.spy_list
    
    def player_is_spy(self, player_num):
        return player_num in self.spy_list
    
    def get_sorted_players(self, asc = True | False):
        reverse = False if asc else True
        s = sorted(self.suspicion_of_being_spy.items(), key = lambda x: x[1], reverse = reverse)
        return [tup[0] for tup in s]
    
    def get_average_team_sus(self, mission):
        average_team_suspicion = 0
        im_in_mission = False

        for mission_player in mission:
            if mission_player == self.me:
                im_in_mission = True
                continue
            average_team_suspicion += self.suspicion_of_being_spy[mission_player]

        divisor = len(mission) - 1 if im_in_mission else len(mission)

        average_team_suspicion /= divisor

        return average_team_suspicion
    
    def get_total_player_sus(self):
        average = 0
        for player in self.other_players:
            average += self.suspicion_of_being_spy[player]

        average /= len(self.other_players)

        return average


    
    def n_spies_in_mission(self, mission):
        n = 0
        inc_me = False
        for player in mission:
            if self.player_is_spy(player):
                n += 1
            if player == self.me:
                inc_me = True

        return n, inc_me
    
    def get_least_sus_spies(self, n):
        sorted_team_list_asc = self.get_sorted_players(asc = True)
        spies = []

        number_returned = 0

        for player in sorted_team_list_asc:
            if self.player_is_spy(player):
                number_returned += 1
                spies.append(player)

            if number_returned == n:
                break

        return spies

    def get_most_sus_non_spies(self, n):
        sorted_team_list_desc = self.get_sorted_players(asc = False)
        non_spies = []

        number_returned = 0

        for player in sorted_team_list_desc:
            if not self.player_is_spy(player):
                number_returned += 1
                non_spies.append(player)

            if number_returned == n:
                break

        return non_spies
    
    def get_players_with_best_voting_consistency(self):
        return sorted(self.all_votes, key = lambda x: self.all_votes[x]['correct_votes'], reverse = True)
    
    def get_probable_spies(self):
        players_sorted_desc = self.get_sorted_players(asc = False)
        return players_sorted_desc[:self.number_of_spies]
    
    def get_least_sus_non_spies(self, n):
        sorted_team_list_asc = self.get_sorted_players(asc = True)
        non_spies = []

        number_returned = 0

        for player in sorted_team_list_asc:
            if not self.player_is_spy(player):
                number_returned += 1
                non_spies.append(player)

            if number_returned == n:
                break

        return non_spies


    def propose_mission(self, team_size, betrayals_required):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        if self.is_spy():
            # TEST
            # if self.upcoming_mission_number == 1:
            #     return self.get_most_sus_non_spies(team_size-1) + [self.me]
            # if self.upcoming_mission_number >= 2:
            #     will_go_on_mission = random.random() < 0.9
            #     if will_go_on_mission:
            #         spies = self.get_least_sus_spies(betrayals_required-1)
            #         non_spies = self.get_most_sus_non_spies(team_size - (betrayals_required-1))

            #         return spies + non_spies + [self.me]
            #     else:
            #         spies = self.get_least_sus_spies(betrayals_required)
            #         non_spies = self.get_most_sus_non_spies(team_size - (betrayals_required))

            #         return spies + non_spies
            # else:
            #     # if its early, i will not go in the team
            #     spies = self.get_least_sus_spies(betrayals_required)
            #     non_spies = self.get_most_sus_non_spies(team_size - (betrayals_required))

            #     return spies + non_spies

            # if self.number_of_wins == 2: # we need a good team to get the final win
            #     sorted_players_least_first = self.get_sorted_players(asc = False)
            #     best_spy = None

            #     for player in sorted_players_least_first:
            #         if self.player_is_spy(player):
            #             best_spy = player
            #             break


            #     # if betrayals_required == 2:
            #     #     non_spies = self.get_most_sus_non_spies(team_size - 2)
            #     #     return  non_spies + [self.me] + [best_spy]
                
            #     spies = self.get_least_sus_spies(betrayals_required-1)
            #     non_spies = self.get_most_sus_non_spies(team_size - (betrayals_required-1))

            #     return spies + non_spies + [self.me]

            # if self.number_of_wins == 2 and team_size >= 5 and self.upcoming_mission_number >= 4 and self.number_of_spies >= 3:
            #     #print("THREE SPIES")
            #     # 3 spies in this case, if the team is large
            #     # sorted_team_asc = self.get_sorted_players(asc = True)
            #     # spies = self.get_least_sus_spies(2)

            #     # non_spies = []
            #     # n = 0

            #     # for player in sorted_team_asc:
            #     #     if player != self.me and not self.player_is_spy(player):
            #     #         non_spies.append(player)
            #     #         n += 1
            #     #     if n == (team_size-3):
            #     #         break
                
            #     # return spies + [self.me] + non_spies

            #     spies = self.get_least_sus_spies(3)
            #     #non_spies = self.get_most_sus_non_spies(team_size - 3)
            #     non_spies = self.get_least_sus_non_spies(team_size - (3))

            #     # print(spies)
            #     # print(non_spies)
            #     # print("team size ^^:", team_size)
            #     # print(self.suspicion_of_being_spy)
            #     # print(self.spy_list)

            #     return spies + [self.me] + non_spies
                
            
            spies = self.get_least_sus_spies(betrayals_required-1)
            non_spies = self.get_most_sus_non_spies(team_size - (betrayals_required))
            #non_spies = self.get_least_sus_non_spies(team_size - (betrayals_required))

            return spies + non_spies + [self.me]
        else:
            sorted_players_least_first = self.get_sorted_players(asc = True)
            return sorted_players_least_first[:team_size-1] + [self.me]


    def is_sus_team(self, mission, num_betrayals):
            
        team_average_sus = self.get_average_team_sus(mission)
        total_average_player_sus = self.get_total_player_sus()

        player_suses = [self.suspicion_of_being_spy[player] for player in mission if player != self.me]

        # if len(player_suses) >= 2 and stdev(player_suses) > 0.35:
        #     return True



        margin = [0.7, 0.8, 0.9, 0.975, 1.05][self.upcoming_mission_number-1]

        if team_average_sus > total_average_player_sus*margin:
            return True
        
        mission_set = set(mission)
        for team in self.failing_mission_teams:
            if mission_set == team:
                return True
            elif mission_set <= team:
                return True
            
        return False
            
        

    def vote(self, mission, proposer, betrayals_required):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals_required are the number of betrayals required for the mission to fail.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        # average_team_sus = self.get_average_team_sus(mission)
        # total_average_player_sus = self.get_total_player_sus()

        # if average_team_sus > total_average_player_sus:
        #     return False

        # if proposer == self.me:
        #     if self.upcoming_mission_number <= 4:
        #         return True
        #     else:
        #         return random.random() < 0.95
            #return True


        if self.is_spy():


            n_spies_in_mission, inc_me = self.n_spies_in_mission(mission)
            
            if n_spies_in_mission < betrayals_required:
                return False
            
            # if proposer == self.me:
            #     if (n_spies_in_mission-1) >= betrayals_required:

            if self.number_of_wins == 2:
                return True
            
            if proposer == self.me:
                return True
            
            if betrayals_required == n_spies_in_mission:
                return True



            # NEW ADDED
            # if self.number_of_wins == 1 and self.upcoming_mission_number == 2:
            #     return random.random() < 0.5
            
            # if self.number_of_wins == 1 and self.upcoming_mission_number == 3:
            #     return random.random() < 0.2
            
            # if self.number_of_wins == 2 and self.upcoming_mission_number == 3:
            #     return random.random() < 0.1
            
            # if 1 <= self.number_of_wins <= 2 and self.upcoming_mission_number == 4:
            #     return random.random() < 0.4


            
            return True
        
        # if proposer in self.high_chance_spy:
        #     #print("NUP")
        #     return False
        
        # players_sorted_desc = self.get_sorted_players(asc = False)
        # most_sus_player = players_sorted_desc[0]

        # if len(mission) <= 3:
        #     if most_sus_player in mission:
        #         return False
        #     if average_team_sus > total_average_player_sus:
        #         return False

        # if self.upcoming_mission_number == 1:
        #     return True

        # if self.me == proposer:
        #     return True


        is_team_sus = self.is_sus_team(mission, betrayals_required)

        if is_team_sus:
            #print("SUS TEAM")
            return False
        
        # if self.upcoming_mission_number == 1:
        #     return True
        
        probable_spies = self.get_probable_spies()
        probable_spies_in_team = set(probable_spies) & set(mission)

        count_of_def_spies = 0

        for player in probable_spies_in_team:
            if self.is_player_definitely_spy(player):
                #return False
                count_of_def_spies += 1
        
        if count_of_def_spies >= betrayals_required:
            return False
            
        # if proposer in probable_spies and self.upcoming_mission_number >= 4:
        #     return random.random() < 0.5

        # if len(probable_spies_in_team) == 0:
        #     return True
        
        # ADDED, SHOWED SOME PROMISE EXP
        if self.upcoming_mission_number >= 4:
            if len(probable_spies_in_team) == 0:
                return True
            if len(probable_spies_in_team) < betrayals_required:
                #print("HMMMMMM")
                return True
            else:
                return False
            
        if proposer == self.me:
            return True
            
        # if proposer in probable_spies and self.upcoming_mission_number >= 5:
        #     #print("SUS PROPOSER")
        #     return False
        # [W3] 0.5389, 0.5441, 0.5424, 0.5368
        

            
        
        return True#random.random() < 0.8



        # OG
        #return True

    def apply_bayes_rule(self, prior, cond1, cond2):
        posterior = (prior*cond1)/(prior*cond1 + (1-prior)*cond2)
        return posterior


    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # note to self, votes is an array of players (not dict) who voted yes
        self.latest_set_of_votes = set(votes) - {self.me}

        average_team_sus = self.get_average_team_sus(mission)
        total_average_player_sus = self.get_total_player_sus()

        # rate = self.vote_sus_scaling[self.upcoming_mission_number]

        # # NEW TEST
        # #if not self.is_spy():
        no_votes = set(self.other_players) - self.latest_set_of_votes

        if self.is_sus_team(mission, None):
            for player in votes:
                if player != self.me:
                    self.suspicion_of_being_spy[player] = self.apply_bayes_rule(self.suspicion_of_being_spy[player], 0.95, 0.4)
            for player_no in no_votes:
                if player_no != self.me:
                    self.suspicion_of_being_spy[player_no] = self.apply_bayes_rule(self.suspicion_of_being_spy[player_no], 0.2, 0.7)
        # else:
        #     for player in votes:
        #         if player != self.me:
        #             self.suspicion_of_being_spy[player] = self.apply_bayes_rule(self.suspicion_of_being_spy[player], 0.45, 0.55)
        #     for player_no in no_votes:
        #         if player_no != self.me:
        #             self.suspicion_of_being_spy[player_no] = self.apply_bayes_rule(self.suspicion_of_being_spy[player_no], 0.6, 0.45)

            #return

        if proposer == self.me:
            for player in no_votes:
                self.suspicion_of_being_spy[player] = self.apply_bayes_rule(self.suspicion_of_being_spy[player], 0.8, 0.4)
            for player_yes in votes:
                if player_yes != self.me:
                    self.suspicion_of_being_spy[player_yes] = self.apply_bayes_rule(self.suspicion_of_being_spy[player_yes], 0.4, 0.7)
        
        # print("RO ME:", self.me, "SUS:", self.suspicion_of_being_spy)

                #return

            # if self.upcoming_mission_number >= 5:
            #     probable_spies = self.get_probable_spies()
            #     if len(set(probable_spies) & set(mission)) >= 2:
            #         for player in votes:
            #             if player != self.me:
            #                 #print("AHHHHH")
            #                 self.suspicion_of_being_spy[player] *= (1 + rate*1.9)



            




        #nothing to do here
        

    def betray(self, mission, proposer, betrayals_required):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals_required are the number of betrayals required for the mission to fail.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        Only spies are permitted to betray the mission.
        By default, spies will betray 30% of the time. 
        '''
        if not self.is_spy():
            return False
        
        # TEST
        # if self.upcoming_mission_number == 1 and proposer == self.me:
        #     return random.random() < 0.8

        proposer_track_record = sorted(self.proposer_track_record, key = lambda x: self.proposer_track_record[x], reverse = True)
        best_spy = proposer_track_record[0]
        
        n_spies_in_mission, inc_me = self.n_spies_in_mission(mission)

        if n_spies_in_mission < betrayals_required:
            # if we dont have enough spies, then dont betray as i know the mission wont pass
            return False

        # if one more win, puts us over the majority, always vote
        if self.number_of_wins == 2:
            return True
        
        # if self.upcoming_mission_number == 1:
        #     return random.random() < 0.1
        
        # if self.upcoming_mission_number == 2 and self.number_of_wins == 1:
        #     return random.random() < 0.8

        
        
        # if self.upcoming_mission_number == 1:
        #     return False
        
        # if best_spy == proposer and proposer_track_record[best_spy] >= 1 and self.player_is_spy(proposer):
        #     print("BEST SPY")
        #     return True

        # if self.player_is_spy(proposer) and self.number_of_wins == 1:
        #     return random.random() < 0.9

        # if self.upcoming_mission_number == 3 and self.number_of_wins == 2:
        #     return False
        
        
        # n_spies_in_mission, _ = self.n_spies_in_mission(mission)

        # if betrayals_required == 1 and n_spies_in_mission == 2: # if theres another spy which maybe could betray, maybe they will
        #     return random.random() < 0.99
        
        if self.upcoming_mission_number == 1:
            return random.random() < 0.85

        if self.upcoming_mission_number == 2:
            return random.random() < 0.92
        
        if self.upcoming_mission_number == 3:
            return random.random() < 0.94
        
        if self.upcoming_mission_number == 4:
            return random.random() < 0.98

        
        # if len(mission) >= 4:
        #     return random.random() < 0.95
        # else:
        #     return random.random() < 0.80
        
        # if self.number_of_wins == 1:
        #     return random.random() < 0.8
        
        # OG
        #return random.random() < 0.95 # DO NOT MAKE SUPER SUPER HIGH, 0.9 IS PRETTY GOOD

        return True
    #0.4279
    #0.4260

    def update_voting_history(self, mission_success):
        for player in self.other_players:
            if not mission_success:
                if player in self.latest_set_of_votes:
                    self.all_votes[player]['incorrect_votes'] += 1
                else:
                    self.all_votes[player]['correct_votes'] += 1
            else:
                if player in self.latest_set_of_votes:
                    self.all_votes[player]['correct_votes'] += 1
                else:
                    self.all_votes[player]['incorrect_votes'] += 1

    def analyse_mission_teams(self):
        if len(self.failing_mission_teams) == 0:
            return None
        
        players_in_all_failing_missions = self.failing_mission_teams[0]

        for mission in self.failing_mission_teams[1:]:
            players_in_all_failing_missions = players_in_all_failing_missions.intersection(mission)

        if len(players_in_all_failing_missions) >= 1:
            return players_in_all_failing_missions
        
    def analyse_mission_votes(self):
        if len(self.failing_votes_teams) == 0:
            return None
        
        players_with_all_wrong_votes = self.failing_votes_teams[0]

        for mission in self.failing_votes_teams[1:]:
            players_with_all_wrong_votes = players_with_all_wrong_votes.intersection(mission)

        if len(players_with_all_wrong_votes) >= 1:
            return players_with_all_wrong_votes
        
    def is_player_definitely_spy(self, player):
        # just because it returns false doesnt mean they are not a spy, it just meant
        # we havent 100% confirmed they are a spy
        return self.suspicion_of_being_spy[player] == float('inf')







    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        num_betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It is not expected or required for this function to return anything.
        '''
        #print("HUH")
        # STATIC: 0.4839, 0.4788, 0.4827 (better) [WO] 0.4744, 0.4862, 0.4887, 0.4847 [WO_S_0.9] 0.4809, 0.4809, 0.4829 [WO_S_0.5] 0.4865, 0.4802, 0.4851
        # SUS-CHANGE: 0.4741, 0.4811, 0.4838 [WO]
        # SUS-CHANGE-MUL: 0.4802, 0.4751, 0.4735
        # sus_change = num_betrayals/(len(mission))
        # if self.me in mission and not self.is_spy():
        #     sus_change = num_betrayals/(len(mission)-1)

        if len(mission) == num_betrayals:
            for p in mission:
                if p != self.me:
                    self.suspicion_of_being_spy[p] = 100#float('inf')


        if self.me in mission:
            sus_change = num_betrayals/(len(mission)-1)
            if len(mission) == 2 and "not self.is_spy()" and not mission_success:
                p1 = mission[0]
                p2 = mission[1]
                if p1 == self.me:
                    self.suspicion_of_being_spy[p2] = 100#float('inf')
                else:
                    self.suspicion_of_being_spy[p1] = 100#float('inf')
        else:
            sus_change = num_betrayals/(len(mission))

        rate = self.upcoming_mission_number/5

        for player in mission:
            if player == self.me:
                continue

            if not mission_success:
                p_failure_given_spy = 0.95 if self.upcoming_mission_number >= 3 else 0.9
                p_spy_prior = self.suspicion_of_being_spy[player]
                p_failure_given_not_spy = 0.4 if self.upcoming_mission_number >= 3 else 0.45
                p_not_spy_prior = 1 - p_spy_prior

                p_failure = (p_failure_given_spy*p_spy_prior) + (p_failure_given_not_spy*p_not_spy_prior)

                sus_change = ((p_failure_given_spy*p_spy_prior)/p_failure) - p_spy_prior

                self.suspicion_of_being_spy[player] += sus_change*1#(p_failure_given_spy*p_spy_prior)/p_failure
            else:
                p_success_given_spy = 0.2 if self.upcoming_mission_number >= 3 else 0.3
                p_spy_prior = self.suspicion_of_being_spy[player]
                p_success_given_not_spy = 0.75 if self.upcoming_mission_number >= 3 else 0.7
                p_not_spy_prior = 1 - p_spy_prior

                p_success = (p_success_given_spy * p_spy_prior) + (p_success_given_not_spy * p_not_spy_prior)

                sus_change = ((p_success_given_spy*p_spy_prior)/p_success) - p_spy_prior

                self.suspicion_of_being_spy[player] += sus_change*1#(p_success_given_spy * p_spy_prior) / p_success

        # # now do the voting bit
        no_votes = set(self.other_players) - self.latest_set_of_votes

        for player in self.other_players:
            # aims to find P(spy|yes_vote,mission_outcome), the outcome could be success or failure
            is_yes_vote = True if player in self.latest_set_of_votes else False

            p_spy_prior = self.suspicion_of_being_spy[player]
            p_not_spy_prior = 1 - p_spy_prior

            if not mission_success:
                if is_yes_vote:
                    # wrong vote
                    p_vote_and_failed_mission_given_spy = 0.95 if self.upcoming_mission_number >= 3 else 0.8 #0.85  #P(vote yes and failed mission | spy)
                    p_vote_and_failed_mission_given_not_spy = 0.2 if self.upcoming_mission_number >= 3 else 0.4 #0.45  #P(vote yes and failed mission | not spy)
                else:
                    # correct vote
                    p_vote_and_failed_mission_given_spy = 0.2 if self.upcoming_mission_number >= 3 else 0.4  #P(vote no and failed mission | spy)
                    p_vote_and_failed_mission_given_not_spy = 0.95 if self.upcoming_mission_number >= 3 else 0.8  #P(vote no and failed mission | not spy)

                p_vote_and_failed_mission = (p_vote_and_failed_mission_given_spy * p_spy_prior) + \
                                            (p_vote_and_failed_mission_given_not_spy * p_not_spy_prior)
                
                sus_change = ((p_vote_and_failed_mission_given_spy*p_spy_prior)/p_vote_and_failed_mission) - p_spy_prior

                reduce_sus = 0.90 if not is_yes_vote else 1

                self.suspicion_of_being_spy[player] += sus_change*1*1#(p_vote_and_failed_mission_given_spy * p_spy_prior) / p_vote_and_failed_mission

            else:
                if is_yes_vote:
                    # correct vote
                    p_vote_and_success_mission_given_spy = 0.2 if self.upcoming_mission_number >= 3 else 0.4
                    p_vote_and_success_mission_given_not_spy = 0.95 if self.upcoming_mission_number >= 3 else 0.8
                else:
                    # wrong vote
                    p_vote_and_success_mission_given_spy = 0.95 if self.upcoming_mission_number >= 3 else 0.8
                    p_vote_and_success_mission_given_not_spy = 0.2 if self.upcoming_mission_number >= 3 else 0.4

                p_vote_and_success_mission = (p_vote_and_success_mission_given_spy * p_spy_prior) + \
                                            (p_vote_and_success_mission_given_not_spy * p_not_spy_prior)
                
                sus_change = ((p_vote_and_success_mission_given_spy*p_spy_prior)/p_vote_and_success_mission) - p_spy_prior

                reduce_sus = 0.90 if is_yes_vote else 1

                self.suspicion_of_being_spy[player] += sus_change*1*1#(p_vote_and_success_mission_given_spy * p_spy_prior) / p_vote_and_success_mission

        if proposer == self.me:
            return
        
        scaling_factors = [0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
        scaling_factor = scaling_factors[self.upcoming_mission_number]

        if not mission_success:
            p_propose_fail_given_spy = 0.95 if self.upcoming_mission_number >= 3 else 0.75
            p_propose_fail_given_not_spy = 0.3 if self.upcoming_mission_number >= 3 else 0.5
        else:
            p_propose_success_given_spy = 0.1 if self.upcoming_mission_number >= 3 else 0.2
            p_propose_success_given_not_spy = 0.7 if self.upcoming_mission_number >= 3 else 0.55

        p_proposer_spy_prior = self.suspicion_of_being_spy[proposer]
        p_proposer_not_spy_prior = 1 - p_proposer_spy_prior

        if not mission_success:
            p_proposal = (p_propose_fail_given_spy * p_proposer_spy_prior) + \
                        (p_propose_fail_given_not_spy * p_proposer_not_spy_prior)
            
            sus_change = ((p_propose_fail_given_spy*p_proposer_spy_prior)/p_proposal) - p_proposer_spy_prior

            self.suspicion_of_being_spy[proposer] += sus_change#*1.15#(p_propose_fail_given_spy * p_proposer_spy_prior) / p_proposal
        else:
            p_proposal = (p_propose_success_given_spy * p_proposer_spy_prior) + \
                        (p_propose_success_given_not_spy * p_proposer_not_spy_prior)
            
            sus_change = ((p_propose_success_given_spy*p_proposer_spy_prior)/p_proposal) - p_proposer_spy_prior
            #print("SUS CHANGE:", sus_change)
            self.suspicion_of_being_spy[proposer] += sus_change#*(1+scaling_factor)#*1.15*0.90#(p_propose_success_given_spy * p_proposer_spy_prior) / p_proposal






        

        

        # print("MO ME:", self.me, "SUS:", self.suspicion_of_being_spy, "YES:", self.latest_set_of_votes)
        # print()
        #print(self.all_votes)

        # ABOVE IS BETTER: [0.8] 0.4949, 0.4917
        # 




        self.upcoming_mission_number += 1
        #nothing to do here
        

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        #nothing to do here
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        #print("ME:", self.me, "SUS:", self.suspicion_of_being_spy)
        #nothing to do here
        pass