1500 words, outlining...
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
Other techniques that could have been attempted include: doing a dictionary of knowledge again, but with bayesian inference. This would be good, but the information would still be symmetric and using it for 