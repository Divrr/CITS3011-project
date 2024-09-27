# Project: The Resistance
**NOTICE:** If any changes to this specification are required, they will be recorded at the top of this document, and an announcement will be made if appropriate. If the change is substantial, an extension on the deadline may be given as appropriate.

This project is to be completed individually.

This project is marked out of a total of 30 marks and is worth 30% of your unit mark.

This project is due at 11:59 pm on October 10th, 2024. The unit coordinator reserves the right to extend this deadline as appropriate. This has already been extended by a week from what was announced at the start of semester.

You are **strongly encouraged** to submit before 15:00 (3:00 pm) on October 10th, as otherwise staff will not be available outside of work hours to help you with any submission issues, and you may receive a late penalty if you are unable to submit by the deadline.

## Description
In this project you are tasked to research, design, and develop an agent for playing The Resistance.

You will be assessed on the performance of the agent you are able to develop and on your written report of the techniques you investigated and developed.

As always, the purpose of this project is to simulate you encountering this as a novel problem. You should not depend on other people's existing solutions or techniques specifically for The Resistance, as reproducing these techniques rather than working on the problem yourself is plagiarism and misconduct.

## Getting Started
Download the attached `the_resistance.zip`.

**NOTE:** The provided testing code only supports Unix systems (Linux or Mac, for example). If you do not already have a working Unix setup, you are presumably using Windows, and I would recommend you use Windows Subsystem for Linux (WSL) for its simplicity of setup.

To build an agent, you should copy the template provided in the `random_agent.py` module to a file with a new name (e.g. `studentnumber_agent.py`). 

That is, you should subclass the Agent class (defined in the `agent.py` module) and fill in the methods there.

For the simulator to pick your agent, it must be in the `agents` directory.
How to run a single game, in a terminal:
```
python3 run_game.py
```
How to run a tournament of games, in a terminal:
```
python3 run_tournament.py
```
Running a tournament will by default run 1000 games and report the win rates for each agent.
Your objective is to maximize your win rate.

## Rules
### Game Rules: The Resistance
- [The Resistance](https://en.wikipedia.org/wiki/The_Resistance_(game)) is a multiplayer game for 5-10 players.
- One third (rounded up) of the players are randomly selected to be government spies, and the remaining players are loyal members of the resistance.
The spies know who all the other spies are, but the resistance members are unable to distinguish the spies.
- The spies are attempting to sabotage the resistance by deliberately failing enough missions to ruin the resistance's plans.

Play proceeds as follows:
1. A player is randomly selected to be the starting leader.
2. The game consists of a series of 5 "missions":
   1. Each mission has a required number of players to send on the mission, and a required number of Fail votes for the mission to fail.
   2. For each mission, a team is selected by the following process:
      1. The current leader proposes a team of players to send on the mission.
      2. All players vote publicly on the proposed team.
      3. If the team is approved, that team is sent on the mission (see below).
      4. If the team is rejected, the next player becomes the leader and proposes their own team.
      5. After four rejected proposals in a row, the fifth proposal is automatically accepted (in the real game, the spies win after five rejections).
   3. The selected team then votes secretly on whether the mission succeeds:
      1. Loyalists can only vote for the mission to succeed.
      2. Spies may choose to vote for the mission to succeed or fail.
      3. The total number of fail votes is revealed, and if it meets the required number of fails for that mission, the mission fails.
3. The spies win if a majority of the 5 missions fail, and the loyalists win if a majority succeed.

### Agent Rules
- Your agent must implement the provided Python interface to take part in the game.
- Agents are time-limited and all actions they take must be completed within 1 second.
- Agents must be single-threaded and not otherwise attempt to circumvent the simulation.
If we believe your agent attempts to violate any of these rules or otherwise undermine the assessment, it may be disqualified and you may receive no mark.

## Report
You are required to write a report detailing the techniques you researched/investigated, your reasoning behind your choice of design and technique, and your assessment of the effectiveness of your agent.
Your report should be **no more than three (3) A4 pages** (there is no minimum length requirement, so long as you cover the requirements given in the rubric).
Your report should be submitted as a PDF.
If it is not submitted as a PDF, it may receive no mark.
If it is over length, it may receive no mark, or be truncated and only partly marked.
If it is illegibly formatted (tiny font, for example) or otherwise unintelligible, it may not receive a mark.

Marking Rubric
This project is marked out of a total of 30 marks and is worth 30% of your unit mark.
Agent	
(+3) Consistently outperforms RandomAgent
(+4) Consistently outperforms BasicAgent
(+5) Consistently outperforms SatisfactoryAgent
(+6) Consistently outperforms hidden reference agent
Report	
(+2) Considers multiple techniques
(+1) Assesses peformance against reference agents
(+2) Discusses merits of multiple techniques
(+2) Justifies why chosen technique should be effective
(+3) Meaningfully compares techniques to justify choice compared to other options
(+2) Assesses relative performance of different techniques

**WARNING:** The reference agents BasicAgent and SatisfactoryAgent have been provided to enable you to assess your code, but if we have reason to believe that you have plagiarized from these agents (for example, just submitting SatisfactoryAgent in order to beat RandomAgent and BasicAgent), you may receive no mark. You should be able to complete this project without even looking at the implementations of these agents. Your agent must be your own original work, as always.

## Submission
This project is due at 11:59 pm on October 10th, 2024. The unit coordinator reserves the right to extend this deadline as appropriate.
You are **strongly encouraged** to submit before 15:00 (3:00 pm) on October 10th, as otherwise staff will not be available outside of work hours to help you with any submission issues, and you may receive a late penalty if you are unable to submit by the deadline.
You should submit exactly the two following files to cssubmit (see link in side panel):
- `studentnumber_agent.py`: Your agent
- `studentnumber_report.pdf`: Your report as a PDF
In both, "studentnumber" should be replaced with your student number.