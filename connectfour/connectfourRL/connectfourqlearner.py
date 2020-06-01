import random
import numpy as np
import math

class ConnectFourQLearner:
    def __init__(self, board):
        self.NUM_BUCKETS = (7, 6)  # one bucket per slot on board (dunno) x 3 states (yellow or red or empty)

        # Number of discrete actions
        self.NUM_ACTIONS = 7 # board is 7 x 6 you can only choose your column not your row

        # Bounds for each discrete state
        self.STATE_BOUNDS = list(zip(board[0], board[5]))

        '''
        Learning related constants
        '''
        self.MIN_EXPLORE_RATE = 0.001
        self.MIN_LEARNING_RATE = 0.2
        self.DECAY_FACTOR = np.prod(board.size, dtype=float) / 10.0

        '''
        Defining the simulation related constants
        '''
        self.NUM_EPISODES = 50000
        self.MAX_T = np.prod(board.size, dtype=int) * 100
        self.STREAK_TO_END = 100
        self.SOLVED_T = np.prod(board.size, dtype=int)

        '''
        Creating a Q-Table for each state-action pair
        '''
        self.q_table = np.zeros(self.NUM_BUCKETS + (self.NUM_ACTIONS,), dtype=float)
                # Instantiating the learning related parameters
        self.learning_rate = self.get_learning_rate(0)
        self.explore_rate = self.get_explore_rate(0)
        self.discount_factor = 0.99
        self.total_reward = 0

    def select_action(self, state):
        # Select a random action
        if random.random() < self.explore_rate:
            action = {'row' : 0, 'col' : 0 }
        # Select the action with the highest q
        else:
            action = int(np.argmax(self.q_table[state]))
        return action


    def get_explore_rate(self, t):
        return max(self.MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/self.DECAY_FACTOR)))


    def get_learning_rate(self, t):
        return max(self.MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/self.DECAY_FACTOR)))


    def state_to_bucket(self, state):
        bucket_indice = []
        for i in range(len(state)):
            if state[i] <= self.STATE_BOUNDS[i][0]:
                bucket_index = 0
            elif state[i] >= self.STATE_BOUNDS[i][1]:
                bucket_index = self.NUM_BUCKETS[i] - 1
            else:
                # Mapping the state bounds to the bucket array
                bound_width = self.STATE_BOUNDS[i][1] - self.STATE_BOUNDS[i][0]
                offset = (self.NUM_BUCKETS[i]-1)*self.STATE_BOUNDS[i][0]/bound_width
                scaling = (self.NUM_BUCKETS[i]-1)/bound_width
                bucket_index = int(round(scaling*state[i] - offset))
            bucket_indice.append(bucket_index)
        return tuple(bucket_indice)

    def save_result(self, result):
            # the initial state
        if(result.isInitialMove):
            state_0 = self.state_to_bucket(result.boardState)
            self.total_reward = 0

            # Observe the result
        state = self.state_to_bucket(result.boardState)
        self.total_reward += result.reward

        # Update the Q based on the result
        best_q = np.amax(self.q_table[state])
        self.q_table[state_0 + (result.action,)] += self.learning_rate * \
            (result.reward + self.discount_factor * (best_q) - self.q_table[state_0 + (result.action,)])

        # Setting up for the next iteration
        state_0 = state

        if result.gameResult == 'WON':
            self.num_streaks += 1

        # Update parameters
        self.explore_rate = self.get_explore_rate(result.moveNumber)
        self.learning_rate = self.get_learning_rate(result.moveNumber)