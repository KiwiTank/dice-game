from dice_game import DiceGame
import numpy as np
from abc import ABC, abstractmethod

# setting a seed for the random number generator gives repeatable results, making testing easier!
#np.random.seed(111)

game = DiceGame()
game.reset()


# tests the game using alternate setups (n times) 
def extended_tests():
    import time
    total_score = 0
    total_time = 0
    n = 100

    print("Testing extended rules – two three-sided dice.")
    print()

    game = DiceGame(dice=2, sides=3)

    start_time = time.process_time()
    test_agent = MyAgent(game)
    total_time += time.process_time() - start_time

    for i in range(n):
        start_time = time.process_time()
        score = play_game_with_agent(test_agent, game)
        total_time += time.process_time() - start_time

        print(f"Game {i} score: {score}")
        total_score += score

    print()
    print(f"Average score: {total_score/n}")
    print(f"Average time: {total_time/n:.5f} seconds")


# run tests (n times) using the standard game rules 
def tests():
    import time

    total_score = 0
    total_time = 0
    n = 100

    np.random.seed(111)

    print("Testing basic rules.")
    print()

    game = DiceGame()

    start_time = time.process_time()
    test_agent = MyAgent(game)
    total_time += time.process_time() - start_time

    for i in range(n):
        start_time = time.process_time()
        score = play_game_with_agent(test_agent, game)
        total_time += time.process_time() - start_time

        print(f"Game {i} score: {score}")
        total_score += score

    print()
    print(f"Average score: {total_score/n}")
    print(f"Total time: {total_time:.4f} seconds")


# agent to run this game 
def play_game_with_agent(agent, game, verbose=False):
    state = game.reset()

    if (verbose): print(f"Testing agent: \n\t{type(agent).__name__}")
    if (verbose): print(f"Starting dice: \n\t{state}\n")

    game_over = False
    actions = 0
    while not game_over:
        action = agent.play(state)
        actions += 1

        if (verbose): print(f"Action {actions}: \t{action}")
        _, state, game_over = game.roll(action)
        if (verbose and not game_over): print(f"Dice: \t\t{state}")

    if (verbose): print(f"\nFinal dice: {state}, score: {game.score}")

    return game.score


class DiceGameAgent(ABC):
    def __init__(self, dice_game):
        self.game = dice_game
        # variable to keep track of how many re-rolls have taken place in the current game
        self.rounds = 0

    @abstractmethod
    def play(self, state):
        pass


class MyAgent(DiceGameAgent):
    def __init__(self, dice_game):
        super().__init__(dice_game)
        # gamma value for use in Bellman equation.
        self.gamma = 0.77
        # dictionary of game states and utility values (initially set to zero)
        self.value = {s: 0 for s in self.game.states}
        # maximum iterations allowed before convergence when finding utility values for each possible game state
        self.max_iter = 1000
        # beginning at zero, this value is used to determine when the utility values have converged sufficiently
        self.delta = 0
        # penalty imports the dice_game penalty applied to this version of the game
        self.penalty = self.game.penalty

        # iterates through each possible state using value iteration, and determines its optimal utility value
        for i in range(self.max_iter):
            next_values = {s: self.get_max_q(s) for s in self.game.states}

            max_q = (max(abs(next_values[s] - self.value[s]) for s in self.game.states))
            self.delta = max_q
            # if the difference between this run and the last is greater than 5, then value iteration continues.
            # otherwise, it ends as sufficient convergence has been achieved.
            if self.delta >= 5:
                self.value = next_values
            else:
                break

    # function to get the utility of an input game state from the self.value dictionary
    def get_utility(self, state):
        return self.value[state]

    # gets the Q-value for a given game state and action to return the optimal policy
    def get_q_value(self, state, action):
        q_value = []
        # if the action is to retain all dice, then the -1 penalty is not applied to the final score, otherwise the
        # penalty is applied multiplied by the number of game rounds currently run.
        if len(action) == len(state):
            q_value = [1 * ((self.game.final_score(state) + (self.rounds * self.penalty)) + (self.gamma * self.get_utility(state)))]
        else:
            for ind, p in enumerate(self.game.get_next_states(action, state)[3]):
                next_state = self.game.get_next_states(action, state)[0][ind]
                q_value.append(p * ((self.game.final_score(next_state) + ((self.rounds - 1) * self.penalty)) + (self.gamma * self.get_utility(next_state))))
        return sum(q_value)

    # returns the optimal policy for a given state given all possible actions from that state
    def get_max_q(self, state):
        max_q = [self.get_q_value(state, a) for a in self.game.actions]
        return max(max_q)

    # function to return the best action for a given state using the optimal policy
    def play(self, state):
        action = {a: self.get_q_value(state, a) for a in self.game.actions}
        best_action = max(action, key=action.get)
        self.rounds -= 1
        return best_action


if __name__ == "__main__":
    print(tests())
