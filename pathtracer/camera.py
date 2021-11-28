from .ray import Ray
from typing import List


class Camera:
    """
    Camera object, that generates initial
    rays and stores the result.
    """

    def __init__(self, camera):
        self._camera = camera

    def generate_initial_rays(self) -> List[Ray]:
        # TODO
        return []
