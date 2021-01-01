from itertools import zip_longest


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
            value = 0.8 * self.prob_dist[index]
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

