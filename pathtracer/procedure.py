from typing import Type

from .scene import Scene


class Configuration:
    max_depth = 4
    samples = 1


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
        scene_file: str,
        resolution: int,
        environment_map: str,
    ):
        """
        Load configuration
        """
        self.scene = Scene.load(scene_file, resolution)
        self.config = Configuration
        self.scene_file = scene_file
        self.resolution = resolution
        # TODO load environment map and sampler

    def render(self, output_file) -> None:
        """
        Run path tracing render
        """
        from .path_trace import path_trace

        image = path_trace(self)
        image.save(output_file)
