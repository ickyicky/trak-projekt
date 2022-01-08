from random import random
import numpy as np


class RandomSampler:
    def __init__(self):
        pass

    def __call__(self, normal: np.array):
        return np.array([random() * 2 - 1 + normal[i] for i in range(3)])
