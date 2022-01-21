from abc import ABC
from dataclasses import dataclass
import numpy as np

@dataclass
class Configuration:
    algorithm : str
    max_depth: int
    samples: int

class Sampler(ABC):
    def __init__(self, n=1):
        self._index = 0
        self._n = n
        self._data = np.array([])
    
    def __next__(self):
        assert self._index < self._n , "no samples left"
        i = self._index
        self._index += 1
        return self._data[i, :]

class RandomSampler(Sampler):
    def __init__(self, n=1):
        Sampler.__init__(self, n)
        self._data = (2 * np.random.random(size=(n, 3)) - 1)

def halton(b, steps):
    """Source: https://en.wikipedia.org/wiki/Halton_sequence"""
    n, d = 0, 1

    A = np.zeros((steps, 1))
    for i in range(steps):
        x = d - n
        if x == 1:
            n = 1
            d *= b
        else:
            y = d // b
            while x <= y:
                y //= b
            n = (b + 1) * y - x
        A[i] = n / d
    return A

class LowDiscrepancySeriesSampler(Sampler):
    def __init__(self, n=1):
        Sampler.__init__(self, n)
        self._data = 2 * np.hstack([halton(2, n), halton(3, n), halton(5, n)]) - 1


AVAILABLE_SAMPLERS = {
    "random": RandomSampler,
    # "stratified": StratifiedSampler,
    # "multijittered": MultijitteredSampler,
    "low_discrepancy": LowDiscrepancySeriesSampler,
}

def sampler_factory(config : Configuration) -> Sampler:
    assert config.algorithm in AVAILABLE_SAMPLERS, "invalid sampler name"
    n = config.samples * (config.max_depth + 1)
    return AVAILABLE_SAMPLERS[config.algorithm](n)
