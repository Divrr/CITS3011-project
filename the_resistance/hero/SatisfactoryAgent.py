from agent import Agent
import random

# Important: Make sure you put your agents in the agents folder, so that the
# game runner code can find them.

class SatisfactoryAgent(Agent):        
    '''A simple agent capable of beating RandomAgent and BasicAgent and not much else'''

    def __init__(self, name='Satisfactory'):
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
        self.num_players = number_of_players
        self.player_number = player_number
        self.spies = set(spy_list)

        self.num_spies = super().spy_count[self.num_players]

        self.successful_missions = 0
        self.failed_missions = 0

    def is_spy(self, player_num = None):
        '''
        returns True iff the given agent is a spy
        '''
        if player_num == None:
            return self.player_number in self.spies
        return player_num in self.spies

    def propose_mission(self, team_size, betrayals_required):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        if self.is_spy():
            team = [self.player_number]
            if betrayals_required == 2:
                other_spies = list(self.spies - {self.player_number})
                team.append(random.choice(other_spies))

            while len(team) < team_size:
                player = random.randrange(self.num_players)
                if player not in team:
                    team.append(player)
            
            random.shuffle(team)
            return team

        # you're not a spy

        team_options = []
        for player in range(self.num_players):
            if not self.is_spy(player):
                team_options.append(player)

        # check, just in case there's a weird error going on
        if len(team_options) < team_size:
            team_options = list(range(self.num_players))

        # remove yourself from the list of options, so that you don't
        # accidentally put yourself on the team twice
        team_options.remove(self.player_number)
        team = random.sample(team_options, team_size-1)

        # add yourself to the team. if you're a good player, you know you are good
        team.append(self.player_number)
        random.shuffle(team)
        return team

    def vote(self, mission, proposer, betrayals_required):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals_required are the number of betrayals required for the mission to fail.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        # count the number spies you know are on this mission
        spy_count = len(set(mission) & self.spies)

        if self.is_spy():
            # approve missions that you know will fail
            if spy_count >= betrayals_required:
                return True
            
            # reject missions that you know will succeed
            return False
        
        # you're not a spy
        
        # reject missions that you know contain spies,
        # or were proposed by spies
        if spy_count > 0 or self.is_spy(proposer):
            return False
            
        # you know you are not a spy, so a mission you are on
        # is more likely to succeed
        if self.player_number in mission:
            return random.random() < 0.9

        # if there's definitely a spy on the mission, reject mission
        players_not_on_mission = self.num_players - len(mission)
        if (players_not_on_mission - 1) < self.num_spies:
            return False
        
        # you're not on the mission, but it's still possible for the mission team
        # to be good. so maybe vote
        return random.random() < 0.33

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        # nothing to do here
        pass

    def betray(self, mission, proposer, betrayals_required):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals_required are the number of betrayals required for the mission to fail.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        Only spies are permitted to betray the mission.
        '''
        # if we're not a spy, we can't betray the mission
        if not self.is_spy():
            return False

        # calculate number of spies on the mission
        spy_count = len(set(mission) & self.spies)

        # if we don't have enough spies to fail the mission, don't betray
        if spy_count < betrayals_required:
            return False

        # if the resistance will win if this mission succeeds, betray
        if self.successful_missions == 2:
            return True
        
        # if the spies will win if this mission fails, betray
        if self.failed_missions == 2:
            return True
        
        # decide if we want this mission to fail
        want_to_fail = False
        if spy_count > 1:
            want_to_fail = True
        elif self.successful_missions > self.failed_missions:
            want_to_fail = True
        elif random.random() < 0.5:
            want_to_fail = True

        # we want to hide that we are a spy, so don't betray the mission
        if not want_to_fail:
            return False

        # betray the mission
        if spy_count == betrayals_required:
            return True
        
        # there are more spies than betrayals_required, so randomise
        return random.random() < 0.5

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        num_betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It is not expected or required for this function to return anything.
        '''
        if self.is_spy() or num_betrayals == 0:
            return

        potential_spies = len(mission)
        if self.player_number in mission:
            potential_spies -= 1

        if num_betrayals >= potential_spies:
            # based on the number of betrayals, you know for certain that
            # every player on this team (except for you) is a spy
            for player in mission:
                if player != self.player_number:
                    self.spies.add(player)

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        self.successful_missions = rounds_complete - missions_failed
        self.failed_missions = missions_failed
        pass
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        # nothing to do here
        pass
