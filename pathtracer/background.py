from .samplers import Configuration
from .ray import Ray
from .bitmap import color

from PIL import Image
import numpy as np


class Background:
    def __init__(self, config: Configuration):
        self.config = config
        self.color = None
        self.environment_map = None

        if config.background_color is not None:
            self.color = lambda x: config.background_color
        elif config.environment_map is not None:
            with Image.open(config.environment_map) as im:
                self.environment_map = np.array(im) / 255
            self.color = self.color_from_map
        else:
            self.color = lambda x: color(0, 0, 0)

    def color_from_map(self, ray: Ray):
        map_x = (
            (np.arctan(ray.direction[1] / ray.direction[0]) / np.pi + 1)
            / 2
            * self.environment_map.shape[1]
        )
        map_y = (
            (np.arctan(ray.direction[2] / ray.direction[0]) / np.pi + 1)
            / 2
            * self.environment_map.shape[0]
        )
        return self.environment_map[int(map_y), int(map_x)]

    def __call__(self, ray: Ray):
        return self.color(ray)
