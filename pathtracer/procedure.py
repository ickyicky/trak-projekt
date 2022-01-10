from typing import Type
from dataclasses import dataclass

from .scene import Scene


@dataclass
class Configuration:
    max_depth: int
    samples: int


class MainProcedure:
    """
    This class represents
    procedure configuration,
    input data parsing and
    execution of path tracing
    algorithm.

    Created object stores all
    local data:
        - scene
        - sampler object
        - environment map
        - camera information
    """

    def __init__(
        self,
        config: Configuration,
        scene_file: str,
        resolution: int,
        environment_map: str,
    ):
        """
        Load configuration
        """
        self.config = config
        self.scene_file = scene_file
        self.resolution = resolution
        self.scene = None
        # TODO load environment map and sampler

    def load_scene(self):
        self.scene = Scene.load(self.scene_file, self.resolution)

    def free_scene(self):
        self.scene = None

    def render(self, output_file) -> None:
        """
        Run path tracing render
        """
        from .path_trace import path_trace

        image = path_trace(self)
        image.save(output_file)
