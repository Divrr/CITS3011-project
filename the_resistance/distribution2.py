# distribution2.py

import os
import itertools
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont

class Distribution:
    def __init__(self, agent_file, contestants_dir, arena, judge, num_plays):
        self.agent_file = agent_file
        self.contestants_dir = contestants_dir
        self.arena = arena
        self.judge = judge
        self.num_plays = num_plays
        self.agent = os.path.join(arena, agent_file)
        self.contestants = self.load_contestants()

    def load_contestants(self):
        contestants = []
        for contestant in os.listdir(self.contestants_dir):
            if contestant.endswith(".py"):
                contestants.append(contestant)
        return contestants

    def generate_combinations(self):
        combinations = []
        for i in range(len(self.contestants) + 1):
            combinations += list(itertools.combinations(self.contestants, i))
        combinations.remove(())
        return combinations

    def run_tournament(self, contestants):
        for contestant in contestants:
            shutil.copyfile(os.path.join(self.contestants_dir, contestant), os.path.join(self.arena, contestant))
        
        result = subprocess.run(["python3", self.judge], input=str(self.num_plays) + "\n", capture_output=True, text=True, check=False)
        stdout = result.stdout
        stderr = result.stderr

        # Process the result (this part can be expanded based on actual requirements)
        return stdout, stderr

    def generate_image(self, combination, result):
        img = Image.new('RGB', (400, 200), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        text = f"Agent: {self.agent_file}\nContestants: {', '.join(combination)}\nResult: {result}"
        d.text((10, 40), text, fill=(255, 255, 0), font=font)
        return img

    def save_images(self):
        combinations = self.generate_combinations()
        for i, combination in enumerate(combinations):
            result, _ = self.run_tournament(combination)
            img = self.generate_image(combination, result)
            img.save(f"combination_{i}.png")

# Example usage
if __name__ == "__main__":
    agent_file = "agent.py"
    contestants_dir = "contestants"
    arena = "arena"
    judge = "judge.py"
    num_plays = 10
    distribution = Distribution(agent_file, contestants_dir, arena, judge, num_plays)
    distribution.save_images()