class Object:
    """
    Geometry object with assigned material
    """

    def __init__(self, geometry):
        self._geometry = geometry

    @property
    def primitives(self):
        return self._geometry.original.primitives
