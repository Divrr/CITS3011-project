import subprocess, os, time, itertools, shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.table import Table
import colorsys
import time
import seaborn as sns

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
agent_names = ["RandomAgent", "BasicAgent", "SatisfactoryAgent", "Adam", "Seth", "Noah"]
agent_files = [f"{name}.py" for name in agent_names]
import matplotlib.colors as mcolors

# Generate a list of base colors
base_colors = list(mcolors.TABLEAU_COLORS.values())

def adjust_color_hue(color, factor):
    rgb = mcolors.to_rgb(color)
    hsv = colorsys.rgb_to_hsv(*rgb)
    adjusted_hsv = (hsv[0] + factor) % 1.0, hsv[1], hsv[2]
    return colorsys.hsv_to_rgb(*adjusted_hsv)

for contestants in combinations:
    winrate_data = []
    avg_winrates = []
    for idx, (agent_file, agent_name) in enumerate(zip(agent_files, agent_names)):
        start = time.time()
        rankings, winrates = get_distribution(agent_file, agent_name, contestants)
        total_winrates, res_win_rates, spy_win_rates = winrates

        # Store data for the violin plot (long-form DataFrame)
        for tw, rw, sw in zip(total_winrates, res_win_rates, spy_win_rates):
            winrate_data.append([agent_name, 'Total', tw])
            winrate_data.append([agent_name, 'Resistance', rw])
            winrate_data.append([agent_name, 'Spy', sw])

        avg_winrates.append([agent_name, np.mean(total_winrates), np.mean(res_win_rates), np.mean(spy_win_rates), np.mean(rankings)])
        print(f'{agent_name} took {time.time() - start:.2f} seconds')

    # Convert the data to a DataFrame for seaborn
    df = pd.DataFrame(winrate_data, columns=['Agent', 'Role', 'Winrate'])

    # Create the violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Agent', y='Winrate', hue='Role', data=df, split=True, palette={'Total': '#5DADE2', 'Resistance': '#28B463', 'Spy': '#CB4335'})

    # Add a horizontal line for the 50% winrate
    plt.axhline(0.5, color='purple', linestyle='dotted', linewidth=1, label='50% Winrate')

    # Set plot labels and title
    plt.title(f'Winrates against {", ".join([contestant.rstrip(".py") for contestant in contestants])}', fontsize=10)
    plt.xlabel('Agent')
    plt.ylabel('Winrate')

    # Adjust legend and save the plot
    plt.legend(loc='upper left')
    plt.savefig(os.path.join(png_dir, f'violin_comparison_{"_".join([agent_name for agent_name in agent_names])}_against_{"_".join(contestants)}.png'))
    plt.close()

    # Create a DataFrame for the average winrates
    avg_df = pd.DataFrame(avg_winrates, columns=['Agent', 'Avg Total Winrate', 'Avg Resistance Winrate', 'Avg Spy Winrate', 'Avg Rank'])

    # Create a table plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    table = Table(ax, bbox=[0, 0, 1, 1])

    # Add table headers
    ncols = len(avg_df.columns)
    nrows = len(avg_df) + 1
    width, height = 1.0 / ncols, 1.0 / nrows

    for i, column in enumerate(avg_df.columns):
        table.add_cell(0, i, width, height, text=column, loc='center', facecolor='lightgrey')

    # Add table data
    for i, row in avg_df.iterrows():
        for j, cell in enumerate(row):
            table.add_cell(i + 1, j, width, height, text=cell, loc='center', facecolor='white')

    ax.add_table(table)
    plt.title('Average Winrates and Rankings')
    plt.savefig(os.path.join(png_dir, f'avg_winrates_table_{"_".join([agent_name for agent_name in agent_names])}_against_{"_".join(contestants)}.png'))
    plt.close()