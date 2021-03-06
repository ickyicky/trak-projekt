from typing import Type

from .samplers import Configuration
from .scene import Scene
from .background import Background


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
    ):
        """
        Load configuration
        """
        self.config = config
        self.scene_file = scene_file
        self.resolution = resolution
        self.scene = None
        self.background = None

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

    def load_background(self):
        self.background = Background(self.config)
