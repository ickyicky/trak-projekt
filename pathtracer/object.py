import numpy as np


class Primitive:
    def __init__(self, primitive):
        self._primitive = primitive
        self._triangles = None
        self._sphere = None

    @property
    def triangles(self):
        if self._triangles is None:
            self._triangles = [x for x in self._primitive]
        return self._triangles

    @property
    def sphere(self):
        if self._sphere is None:
            self.generate_sphere()

        return self._sphere

    def generate_sphere(self):
        vertices = [v for v in self._primitive.vertex]

        center = (
            np.mean([v[0] for v in vertices]),
            np.mean([v[1] for v in vertices]),
            np.mean([v[2] for v in vertices]),
        )


class Object:
    """
    Geometry object with assigned material
    """

    def __init__(self, geometry):
        self._geometry = geometry
        self._primitives = None

    @property
    def primitives(self):
        if self._primitives is None:
            self._primitives = [x for x in self._geometry.primitives()]

        return self._primitives
