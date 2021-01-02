from itertools import zip_longest
import matplotlib.pyplot as plt
import numpy as np


class Filter1D(object):
    """ Represents the measure and move Filter in 1D environment that maps probability distributions """
    def __init__(self, world, prior):
        self.world = world
        self.prob_dist = prior
        self.prob_hit = 0.6
        self.prob_miss = 0.2

    def sense(self, measurement):
        """ Changes probability distribution of location of object with measurement from environment """
        if measurement not in self.world:
            print(f'{measurement} is a false measurement, there is no such in environment.')
        self.prob_dist = [prob * self.prob_hit if measurement == color else prob * self.prob_miss
                          for prob, color in zip(self.prob_dist, self.world)]
        # Normalize posterior probabilities
        self.prob_dist = [prob / sum(prob) for prob in self.prob_dist]

    def move(self, motion):
        """ Moves the object in environment with given motion factor and adds uncertainty around expected position"""
        moved_dist = []
        for idx in range(len(self.prob_dist)):
            index = (idx - motion) % len(self.prob_dist)
            prev_index = (index - 1) % len(self.prob_dist)
            next_index = (index + 1) % len(self.prob_dist)
            # 0.8 is probability factor for exact index
            value = 0.8 * self.prob_dist[index]
            # 0.1 is probability factor for overshoot and undershoot indexes
            value = value + 0.1 * self.prob_dist[next_index]
            value = value + 0.1 * self.prob_dist[prev_index]
            moved_dist.append(value)
        self.prob_dist = moved_dist

    def cycle(self, motions, measurements):
        """ Cycles the sense and move operations of object in environment """
        if len(motions) == len(measurements):
            for motion, measurement in zip(motions, measurements):
                self.sense(measurement)
                self.move(motion)
        # If there is more motions than measurements
        elif len(motions) > len(measurements):
            for motion, measurement in zip_longest(motions, measurements):
                if measurement is not None:
                    self.sense(measurement)
                    self.move(motion)
                else:
                    # Do remaining motion
                    self.move(motion)
        # If there is more measurements than motions
        elif len(motions) < len(measurements):
            for motion, measurement in zip_longest(motions, measurements):
                if motion is not None:
                    self.sense(measurement)
                    self.move(motion)
                else:
                    # Do remaining measurement
                    self.move(measurement)

    def display_map(self, bar_width=1):
        """ Plots the probability distribution of 1D environment """
        if len(self.prob_dist) > 0:
            x = range(len(self.prob_dist))
            plt.bar(x, height=self.prob_dist, bar_width=bar_width, color='brown')
            plt.ylim(0, 1)
            plt.xlabel('Grid Cell')
            plt.ylabel('Probability')
            plt.title('Probability of the object being at each cell in the grid')
            plt.xticks(np.arange(min(self.prob_dist), max(self.prob_dist) + 1, 1))
            if len(self.prob_dist) <= 10:
                print(round(self.prob_dist), 3)
            plt.show()
        else:
            raise ValueError('Probability distribution is empty.')
