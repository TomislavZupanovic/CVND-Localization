from math import sqrt, exp, pi
from itertools import zip_longest
import numpy as np
import matplotlib.pyplot as plt


class Kalman1D(object):
    def __init__(self, init_mean, init_var):
        """ Initialize prior mean and variance """
        self.mean = init_mean
        self.var = init_var

    def gaussian(self, x):
        """ Gaussian Function, for a given mean, variance and x return a Gaussian value """
        coefficient = 1.0 / sqrt(2.0 * pi * self.var)
        exponential = exp(-0.5 * (x - self.mean)**2 / self.var)
        return coefficient * exponential

    def update(self, measurement_mean, measurement_var):
        """ Updates the Gaussian parameters based on a measurements mean and variance after measurement"""
        self.mean = (measurement_var * self.mean + self.var * measurement_mean) / (measurement_var + self.var)
        # Variance is smaller than previous, which means that after measurement we are more certain of location
        self.var = 1 / (1/self.var + 1/measurement_var)

    def predict(self, motion_mean, motion_var):
        """ Updates the Gaussian parameters based on motion mean and variance after motion """
        self.mean += motion_mean
        # Variance is summed, which means that after motion we are more uncertain of location
        self.var += motion_var
