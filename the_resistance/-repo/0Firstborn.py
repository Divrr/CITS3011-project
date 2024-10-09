from agent import Agent
import random

class Firstborn(Agent):
    def __init__(self, name):
        '''
        Initialises the agent, and gives it a name
        You can add configuration parameters etc here,
        but the default code will always assume a 1-parameter constructor, which is the agent's name.
        The agent will persist between games to allow for long-term learning etc.
        '''
        self.name = name

    def __str__(self):
        '''
        Returns a string representation of the agent
        '''
        return "{} {}".format(type(self).__name__, self.name)

    def __repr__(self):
        '''
        returns a representation of the state of the agent.
        default implementation is just the name, but this may be overridden for debugging
        '''
        return self.__str__()

    def new_game(self, number_of_players, player_number, spies):
        '''
        initialises the game, informing the agent of the number_of_players, 
        the player_number (an id number for the agent in the game),
        and a list of agent indexes, which is the set of spies if this agent is a spy,
        or an empty list if this agent is not a spy.
        '''
        self.number_of_players = number_of_players
        self.player_number = player_number
        self.spies = spies
        self.players = list(range(0, number_of_players))
        print("\033[92m New game! I am agent {} of {} \033[0m".format(player_number, number_of_players))

    def propose_mission(self, team_size, betrayals_required):
        '''
        expects a team_size list of distinct agents with id between 0 (inclusive) and number_of_players (exclusive)
        to be returned. 
        betrayals_required are the number of betrayals required for the mission to fail.
        '''
        return random.sample(range(0, self.number_of_players), team_size)

    def vote(self, mission, proposer, betrayals_required):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals_required are the number of betrayals required for the mission to fail.
        The function should return True if the vote is for the mission, and False if the vote is against the mission.
        '''
        return True

    def vote_outcome(self, mission, proposer, votes):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        votes is a dictionary mapping player indexes to Booleans (True if they voted for the mission, False otherwise).
        No return value is required or expected.
        '''
        print("\033[92m Mission {} proposed by {} received votes: {} \033[0m".format(mission, proposer, votes))

    def betray(self, mission, proposer, betrayals_required):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players, and include this agent.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        betrayals_required are the number of betrayals required for the mission to fail.
        The method should return True if this agent chooses to betray the mission, and False otherwise. 
        Only spies are permitted to betray the mission. 
        '''
        return True

    def mission_outcome(self, mission, proposer, num_betrayals, mission_success):
        '''
        mission is a list of agents to be sent on a mission. 
        The agents on the mission are distinct and indexed between 0 and number_of_players.
        proposer is an int between 0 and number_of_players and is the index of the player who proposed the mission.
        num_betrayals is the number of people on the mission who betrayed the mission, 
        and mission_success is True if there were not enough betrayals to cause the mission to fail, False otherwise.
        It is not expected or required for this function to return anything.
        '''
        print("\033[92m Mission {} proposed by {} was a {} with {} betrayals \033[0m".format(mission, proposer, "success" if mission_success else "failure", num_betrayals))

    def round_outcome(self, rounds_complete, missions_failed):
        '''
        basic informative function, where the parameters indicate:
        rounds_complete, the number of rounds (0-5) that have been completed
        missions_failed, the numbe of missions (0-3) that have failed.
        '''
        print("\033[92m Round {} complete with {} missions failed \033[0m".format(rounds_complete, missions_failed))
    
    def game_outcome(self, spies_win, spies):
        '''
        basic informative function, where the parameters indicate:
        spies_win, True iff the spies caused 3+ missions to fail
        spies, a list of the player indexes for the spies.
        '''
        if spies_win:
            print("\033[92m Spies win! Spies were: {} \033[0m".format(spies))
        else:
            print("\033[92m Spies lose! Spies were: {} \033[0m".format(spies))
