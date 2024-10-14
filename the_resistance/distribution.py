import subprocess, os, time, itertools, shutil
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.table import Table
import colorsys
import time

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

# for i in range(len(contestants)+1):
#     combinations += list(itertools.combinations(contestants, i))

# combinations.remove(())

combinations = [contestants]

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

# Generate a list of base colors
base_colors = list(mcolors.TABLEAU_COLORS.values())

def adjust_color_hue(color, factor):
    rgb = mcolors.to_rgb(color)
    hsv = colorsys.rgb_to_hsv(*rgb)
    adjusted_hsv = (hsv[0] + factor) % 1.0, hsv[1], hsv[2]
    return colorsys.hsv_to_rgb(*adjusted_hsv)

for contestants in combinations:
    plt.figure(figsize=(10, 6))
    avg_winrates = []

    for idx, (agent_file, agent_name) in enumerate(zip(agent_files, agent_names)):
        start = time.time()
        rankings, winrates = get_distribution(agent_file, agent_name, contestants)
        total_winrates, res_win_rates, spy_win_rates = winrates

        base_color = base_colors[idx % len(base_colors)]  # Cycle through base colors
        total_color = adjust_color_hue(base_color, 0.00)  # No hue adjustment for total winrate
        res_color = adjust_color_hue(base_color, -0.02)    # Slight hue adjustment for resistance winrate
        spy_color = adjust_color_hue(base_color, 0.02)    # Slight hue adjustment for spy winrate

        plt.hist(total_winrates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label=f'{agent_name} Total Winrate', range=(0, 1), color=total_color)
        plt.hist(res_win_rates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label=f'{agent_name} Resistance Winrate', range=(0, 1), color=res_color)
        plt.hist(spy_win_rates, bins=NUM_HIST_BINS, edgecolor='black', alpha=0.5, label=f'{agent_name} Spy Winrate', range=(0, 1), color=spy_color)

        avg_winrates.append([agent_name, np.mean(total_winrates), np.mean(res_win_rates), np.mean(spy_win_rates), np.mean(rankings)])
        print(f'{agent_name} took {time.time() - start:.2f} seconds')

    plt.axvline(0.5, color='purple', linestyle='dotted', linewidth=1, label='50% Winrate')

    plt.title(f'Winrates against {", ".join([contestant.rstrip(".py") for contestant in contestants])}', fontsize=10)
    plt.xlabel('Winrate')
    plt.ylabel('Frequency')

    # Add legends for winrates and ranks
    winrate_legend = "\n".join([f'{agent_name}: Total={total:.2f}, Res={res:.2f}, Spy={spy:.2f}' for agent_name, total, res, spy, _ in avg_winrates])
    rank_legend = "\n".join([f'{agent_name}: Avg Rank={rank:.2f}' for agent_name, _, _, _, rank in avg_winrates])
    plt.figtext(0.99, 0.01, winrate_legend, horizontalalignment='right', fontsize=8, bbox=dict(facecolor='white', alpha=0.5))
    plt.figtext(0.01, 0.01, rank_legend, horizontalalignment='left', fontsize=8, bbox=dict(facecolor='white', alpha=0.5))

    plt.legend(loc='upper right')

    plt.savefig(os.path.join(png_dir, f'comparison_{"_".join([agent_name for agent_name in agent_names])}_against_{"_".join(contestants)}.png'))
    plt.close()
