import random
import math
import csv

class ConnectFourQLearner:
    def __init__(self):
        self.q = {}
        '''
        Learning related constants
        '''
        self.MIN_EXPLORE_RATE = 0.001
        self.MIN_LEARNING_RATE = 0.2

        '''
        Defining the simulation related constants
        '''
        self.NUM_EPISODES = 50000
        self.STREAK_TO_END = 100

        # Instantiating the learning related parameters
        self.learning_rate = self.get_learning_rate(0)
        self.explore_rate = self.get_explore_rate(0)
        self.discount_factor = 0.99
        self.total_reward = 0
        self.actions = [0,1,2,3,4,5,6]

        with open('dict.csv') as csv_file:
            reader = csv.reader(csv_file)
            self.q = dict(reader)


    def select_action(self, state):
        # Select a random action
        if random.random() < self.explore_rate:
            return {'col' : random.randint(0,6) }
        # Select the action with the highest q
        else:
            stateSanitized = tuple(tuple(x) for x in state)
            qs = [self.getQ(stateSanitized, a) for a in self.actions]
        return {'col' : int(max(qs)) }

    def getQ(self, state, action):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values

        if self.q.get((state, action)) is None:
            self.q[(state, action)] = 1.0
        return self.q.get((state, action))

    def learn(self, board, previousBoard, chosen_action, result):
        """
        Determine the reward based on its current chosen action and update
        the Q table using the reward recieved and the maximum future reward
        based on the resulting state due to the chosen action
        """
        reward = 0
        if (result.get("gameOver")):
            win_value = result.get("winner")
            if win_value == 0:
                reward = 0.5
            elif win_value == 1:
                reward = 1
            else:
                reward = -2
        prev_state = tuple(tuple(x) for x in previousBoard)
        prev = self.getQ(prev_state, chosen_action)
        result_state = tuple(tuple(x) for x in board)
        maxqnew = max([self.getQ(result_state, a) for a in self.actions])
        self.q[(prev_state, chosen_action)] = prev + self.learning_rate * ((reward + self.discount_factor*maxqnew) - prev)
        self.saveLearnings()

    def saveLearnings(self):
        with open('dict.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.q.items():
                writer.writerow([key, value])

    def get_explore_rate(self, t):
        return max(self.MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/0.99)))


    def get_learning_rate(self, t):
        return max(self.MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/0.99)))