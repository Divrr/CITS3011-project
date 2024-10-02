from agent import Agent
import random, signal, functools

TIME_LIMIT = 1 # seconds

# symbol for recognising when a timeout has happened
TIMED_OUT = -1

# based on answer in https://stackoverflow.com/questions/75928586/how-to-stop-the-execution-of-a-function-in-python-after-a-certain-time
def timeout(seconds=TIME_LIMIT, default=TIMED_OUT):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def handle_timeout(signum, frame):
                raise TimeoutError()
            
            try:
                signal.signal(signal.SIGALRM, handle_timeout)
                signal.alarm(seconds)

                result = func(*args, **kwargs)

                signal.alarm(0)

            except TimeoutError:
                result = default

            return result
        
        return wrapper
    
    return decorator

@timeout()
def _time_limit(function, *args):
    return function(*args)

class AgentHandler(Agent):
    def __init__(self, agent):
        self.agent = agent
        self.errors = 0

    def reset_error_counter(self):
        self.errors = 0
    
    def time_limit(self, function, *args):
        result = _time_limit(function, *args)

        if result == TIMED_OUT:
            print("{} exceeded {}s time limit!".format(function, TIME_LIMIT))
            self.errors += 1
            return None
        
        return result

    def __str__(self):
        return str(self.agent)

    def __repr__(self):
        return repr(self.agent)

    def new_game(self, number_of_players, player_number, spy_list):
        self.number_of_players = number_of_players

        # apply a time limit to the agent performing new_game
        self.time_limit(self.agent.new_game, number_of_players, player_number, spy_list)

    def propose_mission(self, team_size, betrayals_required):
        # apply a time limit to the agent performing propose_mission
        result = self.time_limit(self.agent.propose_mission, team_size, betrayals_required)

        # check if processing was actually completed
        if result is not None:
            # check if the result is a valid team proposal
            try:
                if len(result) == team_size and len(set(result)) == team_size:
                    for player_id in result:
                        if not (0 <= player_id < self.number_of_players):
                            break
                    else:
                        # the proposed team is valid!
                        return result
            except TypeError as e:
                print("{} {}".format(self.agent.propose_mission, e))
                self.errors += 1
        
        # either the agent didn't complete processing
        # or there was something wrong with the returned team list
        # so, generate a random team
        return random.sample(range(0, self.number_of_players), team_size)

    def vote(self, *args):
        # apply a time limit to the agent performing vote
        result = self.time_limit(self.agent.vote, *args)

        # if processing was not completed, act as a RandomAgent
        if result is None:
            return random.random() < 0.5
        return result

    def vote_outcome(self, *args):
        # apply a time limit to the agent performing vote_outcome
        self.time_limit(self.agent.vote_outcome, *args)

    def betray(self, *args):
        # apply a time limit to the agent performing betray
        result = self.time_limit(self.agent.betray, *args)

        # if processing was not completed, act like a RandomAgent
        if result is None:
            return random.random() < 0.3
        return result

    def mission_outcome(self, *args):
        # apply a time limit to the agent performing mission_outcome
        self.time_limit(self.agent.mission_outcome, *args)

    def round_outcome(self, *args):
        # apply a time limit to the agent performing round_outcome
        self.time_limit(self.agent.round_outcome, *args)
    
    def game_outcome(self, *args):
        # apply a time limit to the agent performing game_outcome
        self.time_limit(self.agent.game_outcome, *args)
