import pkgutil, importlib, inspect, random, math

from game import Game
from agent import Agent
from agent_handler import AgentHandler

# Important: Make sure you put your agents in the agents folder, so that the
# game runner code can find them.

NUMBER_OF_GAMES = int(input())

# set this to true if you want to see what happens in every game
PRINT_GAME_EVENTS = False

LEADERBOARD_LINES = 50
LEADERBOARD_WIDTH = 200

# list the names of agents you wish to ignore (class name, as string. such as "RandomAgent")
IGNORE_AGENTS = []

################################################################################

agent_name_length = 0
agent_fullname_length = 0

agent_classes = []
agent_pool = []

agent_class_names = set()
agent_class_fullnames = {}
duplicates_exist = False

# find agents in the agents folder
for item in pkgutil.iter_modules(["agents"]):
    package_name = "agents.{}".format(item.name)
    package = importlib.import_module(package_name)
    for name, cls in inspect.getmembers(package, inspect.isclass):
        if issubclass(cls, Agent) and cls is not Agent:
            if name in IGNORE_AGENTS:
                continue

            if name in agent_class_names:
                duplicates_exist = True
            agent_class_names.add(name)

            print("found agent:", name, cls)
            agent_classes.append(cls)

            if len(name) > agent_name_length:
                agent_name_length = len(name)

            fullname = cls.__module__ + "." + cls.__name__
            agent_class_fullnames[cls] = fullname
            if len(fullname) > agent_fullname_length:
                agent_fullname_length = len(fullname)

def create_agent(agent_cls):
    agent_name = "{}{}".format(agent_cls.__name__[:3].lower(), len(agent_pool))
    agent = agent_cls(name=agent_name)
    
    agent = AgentHandler(agent)
    agent.orig_class = agent_cls
    return agent

def print_leaderboard(scores):
    leaderboard = []

    for agent_cls in agent_classes:
        agent_scores = scores[agent_cls]
        win_rate = agent_scores["wins"] / agent_scores["games"] if agent_scores["games"] else 0
        res_win_rate = agent_scores["res_wins"] / agent_scores["res"] if agent_scores["res"] else 0
        spy_win_rate = agent_scores["spy_wins"] / agent_scores["spy"] if agent_scores["spy"] else 0

        # if there are multiple agents with the same class name, show fullnames instead of class names
        if duplicates_exist:
            agent_name = ("{:" + str(agent_fullname_length) + "}").format(agent_class_fullnames[agent_cls])
        else:
            agent_name = ("{:" + str(agent_name_length) + "}").format(agent_cls.__name__)

        leaderboard_line = ("{} | win_rate={:.4f} res_win_rate={:.4f} spy_win_rate={:.4f} | {}").format(
                            agent_name, win_rate, res_win_rate, spy_win_rate,
                            " ".join("{}={}".format(key, agent_scores[key]) for key in agent_scores))

        leaderboard.append((-win_rate, leaderboard_line))

    leaderboard.sort()
    leaderboard = leaderboard[:LEADERBOARD_LINES]

    print("\nLEADERBOARD AFTER {} GAMES".format(scores["games"]))
    print("Resistance Wins: {}, Spy Wins: {}, Resistance Win Rate: {:.4f}".format(scores["res_wins"], scores["spy_wins"], scores["res_wins"]/scores["games"]))
    for i, item in enumerate(leaderboard):
        _, line = item
        print("{:2}: {}".format(i+1, line)[:LEADERBOARD_WIDTH])

# generate agent objects for use in games
number_of_duplicates = math.ceil(10 / len(agent_classes))
for agent_cls in agent_classes:
    for i in range(number_of_duplicates):
        agent_pool.append(create_agent(agent_cls))

# for recording results of games
scores = {agent_cls: {
    "errors": 0,
    "games": 0, "wins": 0, "losses": 0, "res": 0, "spy": 0,
    "res_wins": 0, "res_losses": 0, "spy_wins": 0, "spy_losses": 0,
    } for agent_cls in agent_classes}
scores["games"] = 0
scores["res_wins"] = 0
scores["spy_wins"] = 0

# run the games
print()
for game_num in range(NUMBER_OF_GAMES):
    number_of_players = random.randint(5, 10)
    agents = random.sample(agent_pool, number_of_players)

    if PRINT_GAME_EVENTS:
        if duplicates_exist:
            agents_string = ", ".join(["{} {}".format(agent_class_fullnames[agent.orig_class], agent.agent.name) for agent in agents])
        else:
            agents_string = ", ".join([str(agent) for agent in agents])

        print("\nstarting game size={}, agents=[{}]".format(number_of_players, agents_string))
    
    game = Game(agents)
    game.play()

    if PRINT_GAME_EVENTS:
        print(game)

    # update the scores
    resistance_victory, winning_team, losing_team = game.get_results()

    # overall game stats
    scores["games"] += 1
    if resistance_victory:
        scores["res_wins"] += 1
    else:
        scores["spy_wins"] += 1
    
    # agent stats
    for agent in agents:
        agent_scores = scores[agent.orig_class]
        agent_scores["games"] += 1
        # an agent's "games" count may be higher than the actual number of games
        # this is because multiple instances of the same agent may be present in
        # a game. each participation is counted.

        agent_scores["errors"] += agent.errors
        agent.reset_error_counter()

    for agent in winning_team:
        agent_scores = scores[agent.orig_class]
        agent_scores["wins"] += 1
        if resistance_victory:
            agent_scores["res"] += 1
            agent_scores["res_wins"] += 1
        else:
            agent_scores["spy"] += 1
            agent_scores["spy_wins"] += 1

    for agent in losing_team:
        agent_scores = scores[agent.orig_class]
        agent_scores["losses"] += 1
        if resistance_victory:
            agent_scores["spy"] += 1
            agent_scores["spy_losses"] += 1
        else:
            agent_scores["res"] += 1
            agent_scores["res_losses"] += 1

    if (game_num+1) % 10 == 0:
        print_leaderboard(scores)

if NUMBER_OF_GAMES % 10 != 0:
    print_leaderboard(scores)
