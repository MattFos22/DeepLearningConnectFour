import random
import numpy as np

class ConnectFourQLearner:
    def __init__(self, board):
        NUM_BUCKETS = (7, 6)  # one bucket per slot on board (dunno) x 3 states (yellow or red or empty)

        # Number of discrete actions
        NUM_ACTIONS = 7 # board is 7 x 6 you can only choose your column not your row

        # Bounds for each discrete state
        STATE_BOUNDS = list(zip(board[0], board[5]))

        '''
        Learning related constants
        '''
        MIN_EXPLORE_RATE = 0.001
        MIN_LEARNING_RATE = 0.2
        DECAY_FACTOR = np.prod(board.size, dtype=float) / 10.0

        '''
        Defining the simulation related constants
        '''
        NUM_EPISODES = 50000
        MAX_T = np.prod(board.size, dtype=int) * 100
        STREAK_TO_END = 100
        SOLVED_T = np.prod(board.size, dtype=int)

        '''
        Creating a Q-Table for each state-action pair
        '''
        q_table = np.zeros(NUM_BUCKETS + (NUM_ACTIONS,), dtype=float)


    def select_action(self, state, explore_rate):
        # Select a random action
        if random.random() < self.explore_rate:
            action = 0
        # Select the action with the highest q
        else:
            action = int(np.argmax(self.q_table[state]))
        return action


    def get_explore_rate(t):
        return max(MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))


    def get_learning_rate(t):
        return max(MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/DECAY_FACTOR)))


    def state_to_bucket(state):
        bucket_indice = []
        for i in range(len(state)):
            if state[i] <= STATE_BOUNDS[i][0]:
                bucket_index = 0
            elif state[i] >= STATE_BOUNDS[i][1]:
                bucket_index = NUM_BUCKETS[i] - 1
            else:
                # Mapping the state bounds to the bucket array
                bound_width = STATE_BOUNDS[i][1] - STATE_BOUNDS[i][0]
                offset = (NUM_BUCKETS[i]-1)*STATE_BOUNDS[i][0]/bound_width
                scaling = (NUM_BUCKETS[i]-1)/bound_width
                bucket_index = int(round(scaling*state[i] - offset))
            bucket_indice.append(bucket_index)
        return tuple(bucket_indice)

    def save_result(self, result):
        # Instantiating the learning related parameters
        learning_rate = get_learning_rate(0)
        explore_rate = get_explore_rate(0)
        discount_factor = 0.99

        number_of_wins = 0

            # the initial state
        state_0 = state_to_bucket(obv)
        total_reward = 0

            # Observe the result
        state = state_to_bucket(obv)
        total_reward += reward

        # Update the Q based on the result
        best_q = np.amax(q_table[state])
        q_table[state_0 + (action,)] += learning_rate * (reward + discount_factor * (best_q) - q_table[state_0 + (action,)])

        # Setting up for the next iteration
        state_0 = state

        if done:
            print("Episode %d finished after %f time steps with total reward = %f (streak %d)."
                % (episode, t, total_reward, num_streaks))

            if t <= SOLVED_T:
                num_streaks += 1
            else:
                num_streaks = 0
            break

        elif t >= MAX_T - 1:
            print("Episode %d timed out at %d with total reward = %f."
                % (episode, t, total_reward))

        # It's considered done when it's solved over 120 times consecutively
        if num_streaks > STREAK_TO_END:
            break

        # Update parameters
        explore_rate = get_explore_rate(episode)
        learning_rate = get_learning_rate(episode)