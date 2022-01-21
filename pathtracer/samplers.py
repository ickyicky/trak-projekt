from abc import ABC
from dataclasses import dataclass
import math
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

    def all(self):
        return self._data

    def project_to_sphere(self, points):
        """
        Source: http://extremelearning.com.au/how-to-generate-uniformly-random-points-on-n-spheres-and-n-balls/
        Maps 2D ([0, 1] x [0, 1]) uniformly sampled points to 3D ([-1, 1]^3) uniformly sampled points on a 2-sphere. (Method 10)
        """
        u = points[:, 0]
        v = points[:, 1]

        theta = 2 * np.pi * u
        phi = np.arccos(2 * v - 1)

        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        self._data = np.vstack([x, y, z]).T
        assert self._data.shape == (self._n, 3)
        assert np.allclose(np.linalg.norm(self._data, axis=1), 1)
    
    def __next__(self):
        assert self._index < self._n , "no samples left"
        i = self._index
        self._index += 1
        return self._data[i, :]

class RandomSampler(Sampler):
    def __init__(self, n=1):
        Sampler.__init__(self, n)
        self.project_to_sphere(np.random.random(size=(n, 2)))


def halton(b, steps):
    """
    Source: https://en.wikipedia.org/wiki/Halton_sequence
    """
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

class StratifiedSampler(Sampler):
    def __init__(self, n=1):
        Sampler.__init__(self, n)

        kx = ky = math.isqrt(n)
        if kx * ky < n:
            kx += 1
            ky += 1

        A = np.mgrid[0:1:(1/kx), 0:1:(1/ky)]
        A[0, :, :] = A[0, :, :] + np.random.rand(1, kx, ky)/kx
        A[1, :, :] = A[1, :, :] + np.random.rand(1, kx, ky)/ky

        self.project_to_sphere(A.reshape(2, -1).T[:n, :])

class MultijitteredSampler(Sampler):
    def __init__(self, n=1):
        Sampler.__init__(self, n)

        kx = ky = math.isqrt(n)
        if kx * ky < n:
            kx += 1
            ky += 1

        A = np.mgrid[0:1:(1/kx), 0:1:(1/ky)]
        B = np.random.rand(2, kx, ky)
        B[0, :, :] = B[0, :, :] + np.arange(0, ky).reshape(1, 1, ky)
        B[1, :, :] = B[1, :, :] + np.arange(0, kx).reshape(1, kx, 1)

        A = A + B/(kx * ky)

        # Shuffle
        for i in range(kx):
            A[0, i, 0:ky] = np.random.permutation(A[0, i, :])

        for j in range(ky):
            A[0, 0:kx, j] = np.random.permutation(A[0, :, j])

        self.project_to_sphere(A.reshape(2, -1).T[:n, :])

class LowDiscrepancySeriesSampler(Sampler):
    """
    Requires more samples (>= 20).
    """
    def __init__(self, n=1):
        Sampler.__init__(self, n)
        self.project_to_sphere(np.hstack([halton(2, n), halton(3, n)]))


AVAILABLE_SAMPLERS = {
    "random": RandomSampler,
    "stratified": StratifiedSampler,
    "multijittered": MultijitteredSampler,
    "low_discrepancy": LowDiscrepancySeriesSampler,
}

def sampler_factory(config : Configuration) -> Sampler:
    assert config.algorithm in AVAILABLE_SAMPLERS, "invalid sampler name"
    n = config.samples * (config.max_depth + 1)
    return AVAILABLE_SAMPLERS[config.algorithm](n)
