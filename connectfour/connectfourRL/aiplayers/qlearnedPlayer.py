import random
import csv
import math

class QLearnedPlayer:
    def __init__(self):
        self.loadBrain()
        self.MIN_EXPLORE_RATE = 0.001
        self.MIN_LEARNING_RATE = 0.2
        self.explore_rate = self.get_explore_rate(0)

    def get_explore_rate(self, t):
        return max(self.MIN_EXPLORE_RATE, min(0.8, 1.0 - math.log10((t+1)/0.99)))

    def get_learning_rate(self, t):
        return max(self.MIN_LEARNING_RATE, min(0.8, 1.0 - math.log10((t+1)/0.99)))

    def select_action(self, qTable, state, actions, event, iteration):
        # self.loadBrain()
        # Select a random action
        if random.random() < self.get_explore_rate(iteration):
            return {'col' : random.randint(0,6) }
        # Select the action with the highest q
        else:
            stateSanitized = tuple(tuple(x) for x in state)
            qs = [self.getQ(stateSanitized, a, qTable) for a in actions]
        return {'col' : int(max(qs)) }


    def getQ(self, state, action, qTable):
        """
        Return a probability for a given state and action where the greater
        the probability the better the move
        """
        # encourage exploration; "optimistic" 1.0 initial values

        if qTable.get((state, action)) is None:
            qTable[(state, action)] = 1.0
        return qTable.get((state, action))

    def loadBrain(self):
        #get the brain from one place at the moment - a centralised hive mind!!!!!
        #the qlearner class is currently responsible for saving the brain
        with open('dict.csv') as csv_file:
            reader = csv.reader(csv_file)
            self.q = dict(reader)