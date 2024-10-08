Consumer Of Souls — 02/10/2024 22:04
I guess the problem I can see with q-learning is it needs quite a lot of context to figure stuff out, but you also need to generalise that context to restrict the state-space. I know you're planning on partitioning suspicions, but it feels like the benefits you'd get from RL wouldn't be attributed to just suspicions
But maybe I'm just being pessimistic
I'm interested to see
Ryan1o9 — 02/10/2024 22:05
its slow, but ive got about 362 hours to train :smart:
Consumer Of Souls — 02/10/2024 22:05
I just feel like the optimal strategy with reliable supicions is to vote for the least suspicious people, and the only time that might not be the best is if you know other people on your team are dumb or you don't want to risk a worse team getting in later 
Consumer Of Souls — 02/10/2024 22:05
Damn straight
I need your mindset
Ryan1o9 — 02/10/2024 22:08
but honestly, if the other agents aren't  in the , how would anything be able to get >=60% win rate?
toastA — 02/10/2024 22:08
why q learning just go straight into deep learning
deep reinforcement learning*
Ryan1o9 — 02/10/2024 22:08
✋ 😶 🤚
toastA — 02/10/2024 22:09
first u have to train a neural network
Ryan1o9 — 02/10/2024 22:09
toastA — 02/10/2024 22:10
would be fun ngl
but im hoping around 53% wr is enough to beat the hidden agent
toastA — 02/10/2024 22:34
deep q network
deep RL algorithm that combines q learning with deep neural networks
pretty cool
Consumer Of Souls — 03/10/2024 10:03
Why did he even give us the outcome functions, because I can't really see any easy way to create a learning agent, but it feels like he wants one. Except we can't use it during the competition, so we have to create good agents and train them against each other? Or self-train. I mean I guess we'll see how Ryan's q-learning goes, but currently feels like a red herring
Divrr — 03/10/2024 13:11
PEOPLE
PEOPLE
COME TO THE TUTE
WE ONLY HAVE 3 PEOPLE WE CANT PLAY THE RESISTANCE 😭😭😭
Kirkey — 03/10/2024 13:52
Resistance…is futile
toastA — 03/10/2024 15:59
Wow
Why didn’t u tell me earlier
Divrr — 03/10/2024 16:01
BRUHHH
Anayz — 04/10/2024 13:13
honestly any change i make to my agent only makes it worse
Consumer Of Souls — 04/10/2024 13:24
I feel you
AAA — 04/10/2024 16:31
wait we playing resistance?
Anayz — 04/10/2024 16:56
whats ur guyses best win rate with ur agent, basic agent, random and satisfactory?
Consumer Of Souls — 04/10/2024 19:46
Highest I've hit is 0.55 recently
My newest agent doesn't perform as well which is so depressing
I've spent ages on it
Although it's good at messing with the leaderboard
Like BasicAgent does better than Satisfactory against it
Anayz — 04/10/2024 20:02
The highest I’ve hit is 52% on 10k games
With 1k games it fluctuates a decent amount
Consumer Of Souls — 04/10/2024 20:03
Crying
I don't know if win-rate matters a huge amount
Like if it's everything
The difference also matters
Image
I can't get the worlds thing to work properly
toastA — 04/10/2024 20:05
same
Anayz — 04/10/2024 20:07
I’m tryna get past this 52%
And I think I have to sacrifice some spy win rate to do it
Anayz — 04/10/2024 20:08
Idk what exactly they’re looking for but my best guess is general win rate
Consumer Of Souls — 04/10/2024 20:08
Yeah... Resistance dominate, so it's weighted towards res
Consumer Of Souls — 04/10/2024 20:09
Yeah... It's just on the leaderboard, you can kinda do better just by pushing everyone else down
Anayz — 04/10/2024 20:23
I’ve found that tricky to do without totally tanking the spy win rate
The only way to throw the others off is to be a less than ideal spy
Consumer Of Souls — 04/10/2024 20:27
Nah... It'll have to be resistance stuff that you change
Idk
Anayz — 04/10/2024 20:31
i think i meant to say res lol
like form teams which are maybe not totally perfect
Consumer Of Souls — 05/10/2024 17:08
I've improved my bot, although win-rate has decreased
Anayz — 05/10/2024 17:51
how have u improved it then?
if the win rate has gone down
Consumer Of Souls — 05/10/2024 17:54
It beats my previous agent
By quite a bit
It's better against more rational bots and around the same for shit ones
Anayz — 05/10/2024 18:10
i rly wanna verse some other ppls bots
Anayz — 05/10/2024 18:11
how r u coming up with new agents, are they just all based on different strategies?
Consumer Of Souls — 05/10/2024 18:11
Nah... Just refining my current strat
I don't really know many strategies
Ryan1o9 — Yesterday at 11:31
project when I try to make better agent 
Anayz — Yesterday at 11:44
this is so relatable
Divrr — Yesterday at 11:48
y'all have at least made an agent
that can probably beat the hidden agent just fine
Consumer Of Souls — Yesterday at 12:29
Ah... I've had a breakthrough
It turns out you can't return random.shuffle
Anayz — Yesterday at 12:31
yeah its in place
Consumer Of Souls — Yesterday at 12:32
Yeah
I now have a win rate of 56% with a diff of 10%, though
It turns out you can kinda do logical deduction and just assume spies will vote spies in
And pretty much every agent uses that logic
Besides random
And then eliminate groups based on whether it aligns with their expected behaviour
Anayz — Yesterday at 12:36
so u werent returning a array at all?
Consumer Of Souls — Yesterday at 12:59
Yessir… but it seems like their testing code literally just creates one for you without crashing, which was annoying
Anayz — Yesterday at 13:57
this is in ur propose mission?
toastA — Yesterday at 14:17
can we give information to different versions of our agents in the same game?
toastA — Yesterday at 14:28
@Consumer Of Souls
Anayz — Yesterday at 14:47
idek how youd do that ngl
Anayz — Yesterday at 18:26
bruh legit nothing i add is getting me above 54%
Consumer Of Souls — Yesterday at 18:33
Yeah
Consumer Of Souls — Yesterday at 18:36
Directly, I don't think that would be allowed... Indirectly... maybe? I don't think it would be super useful as ideally your agents should dominate due to their number anyway. If you have more than 2. But you could do something with a suspicion score/similarity score and then group together based on that
toastA — Yesterday at 19:55
yeah you're right i dont think its possible
Consumer Of Souls — Yesterday at 20:15
Image
Lmao
That's not against other agents, btw
Well only one other
Anayz — Yesterday at 20:38
versing random?
How does one get a 99% res win rate crazy
Even with only one other
Consumer Of Souls — Yesterday at 20:51
Nah, one of my other better agents
Random messes it up a bit too much
toastA — Yesterday at 21:06
wtf
how many hours have u spent on this project @Consumer Of Souls
do u just do uni all day everyday?
Consumer Of Souls — Yesterday at 21:06
Way too many
Honestly, though, most of it has been a waste of time
Like this solution only took a day
Consumer Of Souls — Yesterday at 21:07
You've got me... I have no life
toastA — Yesterday at 21:07
damn
well coding is one of the better hobbies
vs something like video games
so good job
Consumer Of Souls — Yesterday at 21:07
Exactly... Oh, I also play videogames
Just not often
toastA — Yesterday at 21:07
i see
Consumer Of Souls — Yesterday at 21:07
But I work out as well
toastA — Yesterday at 21:08
u should apply for faang
Consumer Of Souls — Yesterday at 21:08
I'm balanced
And I consume souls!
Consumer Of Souls — Yesterday at 21:08
Maybe... We all feel the call
toastA — Yesterday at 21:08
its very likely u will get in
Consumer Of Souls — Yesterday at 21:10
As a disclaimer, the reason this is so high is because both agents are really good resistance players... My spies always throw (with a kinda co-operative element), so res can usually spot them in 2 rounds and then it's over. Playing with the sample bots doesn't net anything this high
Anayz — Yesterday at 21:23
yeah, every time i sit to do this project, i end up just running tournaments and scanning the winrates over time lol
and they barely ever change haha
Consumer Of Souls — Yesterday at 21:26
Eventually you'll find one over 60
I believe in you
Anayz — Yesterday at 21:26
the thing is
idk if its an issue with me not using bayes
or if its a strategy problem
Consumer Of Souls — Yesterday at 21:27
I mean Bayes helps a lot if you use it right
Otherwise it can kinda screw you over
But it helps you get away from heuristics which are somewhat hit-or-miss
Like I've done 2 different types of bayes agents
Well 4
But 2 have been good
Anayz — Yesterday at 21:28
ive made 1, but it only applies bayes rule in one place
Consumer Of Souls — Yesterday at 21:28
Yeah, that's the thing
If you're doing bayes singularly, apply it as often as you can
Anayz — Yesterday at 21:28
but my current agent is more general and "judges" you based on many little things u do
Consumer Of Souls — Yesterday at 21:28
Like for every little thing
Consumer Of Souls — Yesterday at 21:28
Yeah, my seventh agent did that
My current doesn't
Anayz — Yesterday at 21:29
hmm
u think using bayes is enough to get an extra 6% win rate, coz i doubt it ngl
Consumer Of Souls — Yesterday at 21:31
Mmm... This is a very simple bayes
Image
Well kinda simple
I will eventually hit 60%
Maybe
But whether it's worth it?
Idk
Anayz — Yesterday at 21:32
yeah
coz i acc think ive got a strat problem
theres no crazy strat plays for my agent
its all pretty generic stuff
Consumer Of Souls — Yesterday at 21:33
Yeah, I'm the same
Heuristics aren't that amazing, I don't think
Anayz — Yesterday at 21:34
ok, ill change back to bayes and see how i go
i went away from it coz i wanted to make a more judgey agent lol
Consumer Of Souls — Yesterday at 21:35
Nah, bayes is great for judging
You can spin up a bunch of conditionals
Like voting for a team that failed
Voting against a team that failed
Voting in line with the best choice
Proposing a team that passed
Anayz — Yesterday at 21:36
yeah my current one does a decent amount of that
but instead of bayes just scales the suspisicion based on other factors
toastA — Yesterday at 21:37
didnt gozz say not to use a learning strat like bayes tho?
Consumer Of Souls — Yesterday at 21:37
Mine doesn't learn anymore
Or at least 8 and 9 don't
Anayz — Yesterday at 21:37
im guessing it only learns within a game
Consumer Of Souls — Yesterday at 21:37
Yeah
Anayz — Yesterday at 21:37
not from between other games
toastA — Yesterday at 21:37
yea
Consumer Of Souls — Yesterday at 21:38
So I have a few probabilities I can mess around with and fine-tune
toastA — Yesterday at 21:38
u gonna train a model to fine tune those parameters?
Consumer Of Souls — Yesterday at 21:39
Of course, of course
All part of the daily grind
toastA — Yesterday at 21:40
respect
what training strat are u gonna use
Consumer Of Souls — Yesterday at 21:40
I think my probabilities don't need to add to 1
That's my new insight
Consumer Of Souls — Yesterday at 21:40
Training my brain
toastA — Yesterday at 21:40
wow
Consumer Of Souls — Yesterday at 21:43
I think evaluating proposals is a dead-end, ngl
Consumer Of Souls — Yesterday at 21:50
Can confirm
Anayz — Yesterday at 21:53
evalutating proposals?
Consumer Of Souls — Yesterday at 21:55
Yeah
Examining anyone from the perspective of them being a spy will always result in the mission looking like it'll fail
Just because everyone includes themselves
Which from a spy perspective is an instant fail
So it's not possible to distinguish until the 4th round, at which point there's no need
All conditionals are proxies
Anayz — Yesterday at 22:28
yeah ive encountered this too
when i need to make a somewhat important decision, i need to restrict it to after the 4th (but sometimes 3rd) round
to give my agent some time to learn
Divrr — Today at 07:00
@Ryan1o9 @percy @toastA @AAA im at uni all day today if you wanna play
(And all day everyday basically)
肖恩 — Today at 11:53
so for the report, we're to talk about more than one strategy, but for the agent code submission, we're to submit the best performing one right?
Divrr — Today at 13:36
yep
guys I genuinely am left bereft I keep trying to make a start on this but don't make a dent
Divrr — Today at 14:06
Image
肖恩 — Today at 14:56
lol how do u get 99% lmao 