class Material:
    def __init__(self, material):
        self._material = material

    @property
    def emmitance(self):
        """
        idk if we can just do it like that
        """
        return self._material.effect.emission[:3]

    @property
    def reflectance(self):
        return self._material.effect.reflectivity or 0
