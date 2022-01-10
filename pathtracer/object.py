import numpy as np


class Object:
    """
    Geometry object with assigned material
    """

    def __init__(self, geometry):
        self._geometry = geometry
        self._sphere = None
        self._primitives = None

    @property
    def primitives(self):
        if self._primitives is None:
            self._primitives = [x for x in self._geometry.primitives()]

        return self._primitives

    @property
    def sphere(self):
        if self._sphere is None:
            self.generate_sphere()

        return self._sphere

    def generate_sphere(self):
        matrix = self._geometry.matrix
        position = [d[-1] for d in matrix][:3]
