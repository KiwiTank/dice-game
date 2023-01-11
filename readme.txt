In order to create an AI that could efficiently return the optimal next move in a dice game, where the object is to return the highest possible sum of a variable number of n-sided
dice, I opted to use a version of the value iteration algorithm. This algorithm first finds the optimal utility for each possible state, which is then used to determine the best 
action given the probability of returning a given future state from the current state's available actions.

The first part of the algorithm effectively sets up the agent to run the game. The code does this by running a for-loop which can be set to a maximum number of iterations, thus 
allowing some control over the length of time that the agent will spend trying to find the optimal utility values for each game state. Within the loop a dictionary is iterated though, 
where each key is a state from all possible game states which is paired with a value initially set at zero. On the first iteration the 'get_max_q' function is called, which gets the maximum 
utility value for a state, given one of the possible actions from that state. This function in turn calls the 'get_q_value' function, which calculates the Q-value component of the Bellman
Equation, whereby the probability of a future state, given the current state and a single action, is multiplied by the expected reward from the future state and the utility value from
the current dictionary of state's utility values set up in the agent initiation step. This last value is multiplied by gamma, a value between 0 and 1, which weights the function towards
either current or future reward states. The results of all possible states of a given action are then summed together to create the output Q-value. The maximum Q-value will give the utility 
of a given state, and it is this value that is iterated over in the initiation stage of the agent. Rewards are calculated by summing the expected result state with the penalty from the number
of rounds already completed at the moment that state might be returned as the result.
Each iteration of this step produces increasing utility values, but the magnitude of each increase lessens with each iteration. Eventually the increase is below a given cutoff value, in this case
5, whereby the algorithm considers the initiation of the optimal utility values to have converged. While a lower cutoff value would create a more optimal set of values, it comes at the cost of 
processing time and in order to keep the initiation step under 30 seconds, a value of 5 was chosen.

The second phase of the algorithm is the 'play' function, which takes a dice state and returns the optimal action for that state, which will be derived from the future state with effectively 
the highest expected value. This is done by creating a dictionary, with all possible actions as keys and a value sourced from the 'value' dictionary which holds the optimal utility for each state.
From this dictionary the maximum value policy key is returned, which is the optimal action to take given the current state. 

Once the functioning algorithm was completed, the last phase required optimising the variables to return the highest possible average score. This was achieved by running 10,000 games using a 
common seed point to allow for equal comparison between results. The principle variable is the value for gamma. The results of various test runs for different values of gamma are given below:


0.9 -
Average score: 12.2213
Total time: 4121.3906 seconds

0.8 -
Average score: 13.1834
Total time: 2639.3125 seconds

0.78 -
Average score: 13.2364
Total time: 2836.1875 seconds

0.77 -
Average score: 13.2364
Total time: 2781.9375 seconds

0.75 -
Average score: 13.2225
Total time: 2690.3438 seconds

0.73 -
Average score: 13.2174
Total time: 2483.2969 seconds

0.7 -
Average score: 13.2078
Total time: 2654.0781 seconds

0.67 -
Average score: 13.1956
Total time: 2196.4531 seconds

0.66 -
Average score: 13.1956
Total time: 2196.2656 seconds

0.65 -
Average score: 13.1842
Total time: 2098.4375 seconds

0.6 -
Average score: 13.0958
Total time: 2179.2500 seconds

Given the results above I decided on a gamma value of 0.77 (which, although returning the same score as 0.78, was slightly faster). A secondary effect of changing the gamma is that processing
time reduces with lower gamma values, as less total games will need to be run on lower values as this favours keeping the current state and thus will reduce the number of iterations run. 

It would be possible to introduce an iterating loop in order to automatically find the optimal value for gamma by comparing output values within the code, but this would come at a significant
processing speed cost, so it was decided to leave this out for this assignment.