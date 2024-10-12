import subprocess, os, time, itertools, shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.table import Table

# =============================

# This python file runs 1000-round games between the agents and all combinations of other agents
# It then prints the distribution of the agents' win rates

# =============================

tournament_judge_file = "run_tournament.py"
tournament_arena_dir = "agents/"
tournament_sideline_dir = "sideline/"
tournament_hero_dir = "hero/"
png_dir = "-png/"
NUM_PLAYS = 1000
NUM_TOURNAMENTS = 30
NUM_HIST_BINS = 100

# =============================

path = os.getcwd()
judge = os.path.join(path, tournament_judge_file)
arena = os.path.join(path, tournament_arena_dir)
sideline = os.path.join(path, tournament_sideline_dir)
hero = os.path.join(path, tournament_hero_dir)

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

def run_tournament(agent_file, agent_name, contestants):
    # Copy hero agent to arena
    shutil.copyfile(os.path.join(hero, agent_file), os.path.join(arena, agent_file))
    
    # Copy sideline agents to arena
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
    
    if total_winrate == 0:
        print("SOMETHING'S GONE WRONG. WINRATE = 0")
    
    # Remove agents from arena
    os.remove(os.path.join(arena, agent_file))
    for contestant in contestants:
        os.remove(os.path.join(arena, contestant))

    return ranking, [total_winrate, res_win_rate, spy_win_rate]

def get_distribution(agent_file, agent_name, contestants):
    total_winrate, res_win_rate, spy_win_rate = [], [], []
    rankings = []
    print(contestants)
    for _ in tqdm(range(NUM_TOURNAMENTS), desc=f""):
        ranking, winrate = run_tournament(agent_file, agent_name, contestants)
        total_winrate.append(winrate[0])
        res_win_rate.append(winrate[1])
        spy_win_rate.append(winrate[2])
        rankings.append(ranking)
    
    return rankings, [total_winrate, res_win_rate, spy_win_rate]

# =============================

# List all agent files in the hero directory
agent_files = [f for f in os.listdir(hero) if f.endswith(".py")]
agent_names = [os.path.splitext(f)[0] for f in agent_files]  # Extract agent names from filenames
import matplotlib.colors as mcolors

# Generate a list of colors
colors = list(mcolors.TABLEAU_COLORS.values())

for contestants in combinations:
    plt.figure(figsize=(10, 6))
    avg_winrates = []

    for idx, (agent_file, agent_name) in enumerate(zip(agent_files, agent_names)):
        rankings, winrates = get_distribution(agent_file, agent_name, contestants)
        total_winrates, res_win_rates, spy_win_rates = winrates

        color = colors[idx % len(colors)]  # Cycle through colors

        plt.hist(total_winrates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label=f'{agent_name} Total Winrate', range=(0, 1), color=color)
        plt.hist(res_win_rates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label=f'{agent_name} Resistance Winrate', range=(0, 1), color=color)
        plt.hist(spy_win_rates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label=f'{agent_name} Spy Winrate', range=(0, 1), color=color)

        avg_winrates.append([agent_name, np.mean(total_winrates), np.mean(res_win_rates), np.mean(spy_win_rates)])

    plt.axvline(0.5, color='purple', linestyle='dotted', linewidth=1, label='50% Winrate')

    plt.title(f'Winrates against {", ".join([contestant.rstrip(".py") for contestant in contestants])}', fontsize=10)
    plt.xlabel('Winrate')
    plt.ylabel('Frequency')

    # Add a table showing average winrates
    table_data = [['Agent', 'Avg Total Winrate', 'Avg Resistance Winrate', 'Avg Spy Winrate']] + avg_winrates
    table = Table(plt.gca(), bbox=[0, -0.3, 1, 0.2])
    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            table.add_cell(i, j, width=1/4, height=0.1, text=cell, loc='center')
    plt.gca().add_table(table)

    plt.savefig(os.path.join(png_dir, f'comparison_{"_".join([agent_name for agent_name in agent_names])}_against_{"_".join(contestants)}.png'))
    plt.close()
