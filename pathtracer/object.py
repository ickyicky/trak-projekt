import numpy as np
from dataclasses import dataclass


@dataclass
class BoundingBox:
    x1: int
    x2: int
    y1: int
    y2: int
    z1: int
    z2: int


class Primitive:
    def __init__(self, primitive):
        self._primitive = primitive
        self._triangles = None
        self._bounding_box = None

    @property
    def triangles(self):
        if self._triangles is None:
            self._triangles = [x for x in self._primitive]
        return self._triangles

    @property
    def bounding_box(self):
        if self._bounding_box is None:
            self.generate_bounding_box()

        return self._bounding_box

    def generate_bounding_box(self):
        vertices = [v for v in self._primitive.vertex]

        self._bounding_box = BoundingBox(
            x1=min((v[0] for v in vertices)),
            x2=max((v[0] for v in vertices)),
            y1=min((v[1] for v in vertices)),
            y2=max((v[1] for v in vertices)),
            z1=min((v[2] for v in vertices)),
            z2=max((v[2] for v in vertices)),
        )


class Object:
    """
    Geometry object with assigned material
    """

    def __init__(self, geometry):
        self._geometry = geometry
        self._primitives = None
        self._bounding_box = None

    @property
    def primitives(self):
        if self._primitives is None:
            self._primitives = [Primitive(x) for x in self._geometry.primitives()]

        return self._primitives

    @property
    def bounding_box(self):
        if self._bounding_box is None:
            self.generate_bounding_box()

        return self._bounding_box

    def generate_bounding_box(self):
        boxes = [p.bounding_box for p in self.primitives]

        self._bounding_box = BoundingBox(
            x1=min((b.x1 for b in boxes)),
            x2=max((b.x1 for b in boxes)),
            y1=min((b.y1 for b in boxes)),
            y2=max((b.y1 for b in boxes)),
            z1=min((b.z1 for b in boxes)),
            z2=max((b.z1 for b in boxes)),
        )
