from typing import Type

from .scene import Scene


class Configuration:
    max_depth = 16


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
        sampler_cls: Type,
        environment_map: str,
    ):
        """
        Load configuration
        """
        self.scene = Scene.load(scene_file)
        self.config = Configuration
        # TODO load environment map and sampler

    def render(self) -> None:
        """
        Run path tracing render
        """
        from .path_trace import path_trace

        return path_trace(self)
