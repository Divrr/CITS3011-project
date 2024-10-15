<!-- 1500 words, outlining...
- What techniques did you investiagte?
- What were your reasoning behind your choice of design and technique?

FOR EACH TECHNIQUE...
- Outline how it works
- What is the merit of this technique?
- Why should it be effective?
- Assess performance against reference

CHOOSING ONE
- Assess relative performance
- Compare techniques to justify choice

# Preamble: Research


# Technique 1: Seth
## How it works
This technique hard-codes the concept of trust.
We assign a trust value of 1 to each agent. This represents the fact that we trust every agent initially.
If a mission fails, we reduce our trust of the proposer, players in the mission, and players who voted for the mission.
We pick and vote for the players who we trust most. This always includes us.

# Technique 2: bayesian network
Problem: it gets too complicated

# Technique 3: meta-knowledge
Problem: the information is, for the most part, symmetrical. So a discrete method does not help. the sums are always 12, 6, 3, or 0.
Why multi-agent mapping was not necessary.
Problem: very slow to update for large player sizes.

# Technique 4: Noah
Realising 1 is not a good 'probability'. The better starting probability is 1/(n-1 choose num_spies)
How to calculate odds? what is normalization? What formula am I using?

explain that you always want to pick the most trusted crew.
explain how it's better than seth.

```py
        spy_threshold = 0.7
        if self.spy_probability(proposer) > spy_threshold:
            return False

        for member in mission:
            if self.spy_probability(member) > spy_threshold:
                return False

        return True
```
wasn't a good way of voting.

# Conclusion: 
Other techniques that could have been attempted include: doing a dictionary of knowledge again, but with bayesian inference. This would be good, but the information would still be symmetric and using it for  -->

# The Resistance: An exploration of AI techniques

The Resistance is a social deduction game where a third of the players are government spies, trying to sabotage a resistance operation by the remaining players, who are resistance members. Spies know who the other spies are, while resistance members do not know anyone’s role except their own. Across 5 rounds, missions teams are proposed by a leader, to be voted for by each player. Missions with majority approval proceed. In a mission, a spy may choose to fail the mission, while a resistance member must always succeed it. The Resistance wins by completing three successful missions, while the Spies win if they sabotage three.

This paper investigates some techniques for implementing an agent for The Resistance. We will look at the following agents:
- **Adam**, an agent that naively codifies trust and follows common strategies in real play.
- **Seth**, an agent that reasons about all agents’ logical beliefs about all possible worlds.
- **Noah**, an agent using bayes rule to codify its own uncertainty about possible worlds.

## Adam
An initial attempt at implementing an effective agent involves mimicking common strategies used in real play. Some of these will be foundational to other agents. For instance, resistance members should always pick the most trusted players for missions and vote no if they believe an agent on a mission is untrustworthy. Disguised as a confident resistance member, spies should likwise pick the most trusted resistance members, but also include trusted spies to fail the mission reducing trust for all those on the mission. A resistance member should always propose missions they are part of, since it is the only certain information they have. Spies should mirror this tactic to appear like a resistance member.

To implement, we use a trust array starting at 1 for all players, dividing by an arbitrary value (for the proposer, voters and players on the mission) whenever a mission fails. When proposing, we sort the array by trust and pick the first N players, or the first B spies and the first N-B non-spies if you are a spy -- where N is the team size and B is the number of betrayals required. When voting as resistance, we vote yes only if each member and the proposer are above a trust threshold. As resistance, we vote for any team that has the potential to fail the mission.

This technique should be effective since it mimics basic strategies of real play. Fig. 1 shows win rates for 30 1000-game tournaments. Adam performs slightly better than Satisfactory and consistently beats all three agents in a tournament containing all three. We will use Adam to compare our future techniques.

## Seth
For Adam, trust was arbitrarily decreased. To improve precision, we considered all possible spy permutations and eliminated those proven impossible. A world is impossible if a failed mission required more betrayals than the number of spies in that mission. For example, a world with (1, 2, 3) as spies is impossible if a failed mission with (3, 4, 5) required 2 betrayals. Trust in each agent is determined by the sum of valid possible worlds where that agent is a spy, forming a discrete “confidence score.”

Despite logical deductions, incomplete information limits our ability to identify spies effectively. Many possible worlds remain valid even after several missions, and outcomes are often ambiguous and uncertain. Without concrete evidence, our deductions are imprecise, leaving high uncertainty in identifying spies.

To address this, we implemented a multi-agent system. We replicated our agent’s possible-worlds data structure for every other agent, assuming they all behave as resistance members, then applied the same logical reasoning. This increased the effectiveness of our deduction, as multiple independent reasoners could 'back up' each other's claims. This increased our agent’s resistance win rate to be comparable to Adam (see Fig. 2) but was computationally expensive and provided no major benefit over the previous technique.

## Noah
Seth discarded impossible worlds, but we can gain more insight by considering probable worlds using Bayesian reasoning.

The sum of all possible worlds must be 1. We remove impossible worlds and normalize the probabilities of the remaining ones. After each mission, we update the probabilities of each possible world based on the outcome (fail or success) using:

\[ P(\text{possible world} | \text{Outcome}) = P(\text{Spy}_A \land \text{Spy}_B \land \ldots \land \text{Spy}_Z | \text{Outcome}) = \prod P(\text{Spy}_i | \text{Outcome}) \]

Where \(\text{Spy}_i\) represents the event that agent \(i\) is a spy. We calculate each value using Bayes’ rule:

\[ P(\text{Spy}_i | \text{Outcome}) = \alpha \langle P(\text{Outcome} | \text{Spy}_i) P(\text{Spy}_i), P(\text{Outcome} | \neg \text{Spy}_i) P(\neg \text{Spy}_i) \rangle \]

Here, \(\alpha\) is the normalization constant. We find \(P(\text{Spy}_i)\) by summing the probabilities of all worlds where \(i\) is a spy and estimate \(P(\text{Outcome} | \text{Spy}_i)\) and \(P(\text{Outcome} | \neg \text{Spy}_i)\). This approach provides degrees of uncertainty about each possible world, helping us make more informed decisions like Adam.

Seth considered and discarded impossible worlds. However, there is more information we are able to deduce from an event if we allow consideration of probable worlds. Our final technique considers a bayesian reasoning agent. 

The sum of all possible worlds must be 1. This means we can remove any impossible world, then apply normalisation to increase the probability of each remaining world accordingly. At the end of each mission, we update our probabilities for each possible world being true given the perceived outcome (fail or success), using the following:

$P(possible world | Outcome) = P(Spy_A ∧ Spy_B ∧ … ∧ Spy_Z | Outcome) = \prod(Spy_i | Outcome)$

Where Spyi represents the event that agent i is a spy. We can calculate each of the values of the equation separately using Bayes’ rule, using notation from Russel and Norvig:

𝐏(Spyi | Outcome)=α ⟨P( Outcome | Spyi )P( Spyi ),P( Outcome | ¬Spyi )P(¬Spyi )⟩

Where  is the normalization constant bringing the sum of the probabilities down to 1. We find P( Spyi ) by summing up the probabilities of all worlds that satisfy it, and give arbitrary estimations for P( Outcome | Spyi ) and P( Outcome | ¬Spyi ). Computing this over the course of the game gives us degrees of uncertainty about each possible world, which we use to make more informed decisions in the same format as Adam.