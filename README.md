# Dicegame using value iteration
This was a project from my MSc in AI to develop a dicegame whereby the system predicts the optimal next move in order to maximise the final score based on these rules:

### Rules
* You start with 0 points
* Roll a number of n-sided dice
* Now choose one of the following:
* Stick by accepting the values shown. If two or more dice show the same values, then all of them are flipped upside down: 1 becomes 6, 2 becomes 5, 3 becomes 4, and vice versa. The total is then added to your points and this is your final score.
* OR reroll the dice. You may choose to hold any combination of the dice on the current value shown. Rerolling costs you 1 point – so during the game and perhaps even at the end your score may be negative. You then make this same choice again.

The file *dicegame.py* contains the main game object *Dicegame*, which has parameters to allow the number of dice, the number of sides on a die, the fairness of the die, and the penalty for holding to be changed.

*dicegame_agent.py* contains the agent that runs the dicegame object and determines the optimal decisions at each stage in the game, returning its score each time it is run. 
