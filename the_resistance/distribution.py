import subprocess, os, time, itertools, shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# =============================

# This python file runs 1000-round games between the agent and all combinations of other agents
# It then prints the distribution of the agent's win rate

# =============================

tournament_judge_file = "run_tournament.py"
tournament_arena_dir = "agents/"
tournament_sideline_dir = "sideline/"
png_dir = "-png/"
agent_file = "3Noah.py"
agent_name = "Noah"
NUM_PLAYS = 100
NUM_TOURNAMENTS = 30
NUM_HIST_BINS = 100

# =============================

path = os.getcwd()
judge = os.path.join(path, tournament_judge_file)
arena = os.path.join(path, tournament_arena_dir)
sideline = os.path.join(path, tournament_sideline_dir)
agent = os.path.join(arena, agent_file)

# =============================

contestants = []
combinations = []

for contestant in os.listdir(sideline):
    if contestant.endswith(".py"):
        contestants.append(contestant)

for i in range(len(contestants)+1):
    combinations += list(itertools.combinations(contestants, i))

combinations.remove(())

# =============================

def run_tournament(agent, contestants):
    for contestant in contestants:
        shutil.copyfile(os.path.join(sideline, contestant), os.path.join(arena, contestant))
        
    result = subprocess.run(["python3", judge], input=str(NUM_PLAYS)+"\n", capture_output=True, text=True, check=False)
    stdout = result.stdout
    stderr = result.stderr

    coming = False
    total_winrate, res_win_rate, spy_win_rate, ranking = 0, 0, 0, 0
    for line in stdout.split("\n"):
        if "LEADERBOARD AFTER "+str(NUM_PLAYS) in line:
            coming = True
        if coming:
            if agent_name in line:
                total_winrate = float(line.split()[3].split("=")[1])
                res_win_rate = float(line.split()[4].split("=")[1])
                spy_win_rate = float(line.split()[5].split("=")[1])
                ranking = int(line.split()[0].strip(":"))
    
    for contestant in contestants:
        os.remove(os.path.join(arena, contestant))

    return ranking, [total_winrate, res_win_rate, spy_win_rate]

def get_distribution(agent, contestants):
    total_winrate, res_win_rate, spy_win_rate = [], [], []
    rankings = []
    print(contestants)
    for _ in tqdm(range(NUM_TOURNAMENTS), desc=f""):
        ranking, winrate = run_tournament(agent, contestants)
        total_winrate.append(winrate[0])
        res_win_rate.append(winrate[1])
        spy_win_rate.append(winrate[2])
        rankings.append(ranking)
    
    return rankings, [total_winrate, res_win_rate, spy_win_rate]

# =============================

for contestants in combinations:
    rankings, winrates = get_distribution(agent, contestants)
    total_winrates, res_win_rates, spy_win_rates = winrates

    plt.hist(total_winrates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label='Total Winrate', color='blue', range=(0, 1))
    plt.hist(res_win_rates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label='Resistance Winrate', color='green', range=(0, 1))
    plt.hist(spy_win_rates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label='Spy Winrate', color='red', range=(0, 1))
    
    plt.axvline(np.mean(total_winrates), color='blue', linestyle='dashed', linewidth=1, label='Average Total Winrate')
    plt.axvline(np.mean(res_win_rates), color='green', linestyle='dashed', linewidth=1, label='Average Resistance Winrate')
    plt.axvline(np.mean(spy_win_rates), color='red', linestyle='dashed', linewidth=1, label='Average Spy Winrate')
    plt.axvline(0.5, color='purple', linestyle='dotted', linewidth=1, label='50% Winrate')
    
    plt.title(f'Winrates against {", ".join([contestant.rstrip(".py") for contestant in contestants])}', fontsize=10)
    plt.xlabel('Winrate')
    plt.ylabel('Frequency')
    plt.legend()
    
    avg_total_winrate = np.mean(total_winrates)
    avg_res_winrate = np.mean(res_win_rates)
    avg_spy_winrate = np.mean(spy_win_rates)
    avg_rankng = np.mean(rankings)
    plt.figtext(0.5, 0.01, f'avg Total Winrate: {avg_total_winrate:.2f}, avg Resistance Winrate: {avg_res_winrate:.2f}, avg Spy Winrate: {avg_spy_winrate:.2f}, avg ranking: {avg_rankng:.2f}', ha='center', fontsize=8, alpha=0.5)
    
    plt.savefig(os.path.join(png_dir, f'{agent_name}_{'_'.join(contestants)}.png'))
    plt.close()