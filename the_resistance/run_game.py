import pkgutil, importlib, inspect, random, math

from game import Game
from agent import Agent
from agent_handler import AgentHandler

# Important: Make sure you put your agents in the agents folder, so that the
# game runner code can find them.

# list the names of agents you wish to ignore (class name, as string. such as "RandomAgent")
IGNORE_AGENTS = []

################################################################################

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

            fullname = cls.__module__ + "." + cls.__name__
            agent_class_fullnames[cls] = fullname

def create_agent(agent_cls):
    agent_name = "{}{}".format(agent_cls.__name__[:3].lower(), len(agent_pool))
    agent = agent_cls(name=agent_name)
    
    agent = AgentHandler(agent)
    agent.orig_class = agent_cls
    return agent

# generate agent objects for use in games
number_of_duplicates = math.ceil(10 / len(agent_classes))
for agent_cls in agent_classes:
    for i in range(number_of_duplicates):
        agent_pool.append(create_agent(agent_cls))

# run the games
number_of_players = random.randint(5, 10)
agents = random.sample(agent_pool, number_of_players)

if duplicates_exist:
    agents_string = ", ".join(["{} {}".format(agent_class_fullnames[agent.orig_class], agent.agent.name) for agent in agents])
else:
    agents_string = ", ".join([str(agent) for agent in agents])

print("\nstarting game size={}, agents=[{}]".format(number_of_players, agents_string))
    
game = Game(agents)
game.play()

print(game)

error_counter = {}

for agent in agents:
    if agent.errors:
        if agent.orig_class in error_counter:
            error_counter[agent.orig_class] += agent.errors
        else:
            error_counter[agent.orig_class] = agent.errors

if error_counter:
    print()
    for agent_cls in error_counter:
        if duplicates_exist:
            agent_name = agent_class_fullnames[agent_cls]
        else:
            agent_name = agent_cls.__name__
        print("{} errors={}".format(agent_name, error_counter[agent_cls]))
