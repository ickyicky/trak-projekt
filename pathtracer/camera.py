from .ray import Ray
from typing import List
import numpy as np


class Camera:
    """
    Camera object, that generates initial
    rays and stores the result.
    """

    def __init__(self, camera, resolution):
        self._camera = camera
        self.resolution = resolution

    @property
    def matrix(self):
        return self._camera.matrix

    @property
    def fov(self):
        return self._camera.xfov or self._camera.yfov

    @property
    def aspect_ratio(self):
        return self._camera.aspect_ratio

    def generate_initial_rays(self) -> List[Ray]:
        image_height = self.resolution
        image_width = int(self.resolution * self.aspect_ratio)

        rays = []

        def normalize(v):
            norm = np.linalg.norm(v, ord=1)
            if norm == 0:
                norm = np.finfo(v.dtype).eps
            return v / norm

        origin = np.matmul(self.matrix, np.array([0, 0, 0, 1]))

        for x in np.arange(image_width):
            for y in np.arange(image_height):
                px = (
                    (2 * ((x + 0.5) / image_width) - 1)
                    * np.tan(self.fov / 2 * np.pi / 180)
                    * self.aspect_ratio
                )
                py = (1 - 2 * ((y + 0.5) / image_width)) * np.tan(
                    self.fov / 2 * np.pi / 180
                )
                direction = np.matmul(self.matrix, np.array([px, py, -1, 1]))
                direction = normalize(direction - origin)

                rays.append(
                    Ray(
                        origin=origin,
                        direction=direction,
                    ),
                )

        return rays
