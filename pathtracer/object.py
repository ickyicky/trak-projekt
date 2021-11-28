class Object:
    """
    Geometry object with assigned material
    """

    def __init__(self, geometry):
        self._geometry = geometry

    def get_materials(self):
        return self.geometry.materialnodebysymbol
