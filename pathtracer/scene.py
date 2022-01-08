from collada import Collada
from typing import List, Tuple, Any, Dict
from .object import Object
from .camera import Camera
from .material import Material


class Scene:
    """
    Wrapper around Collada for storing
    scene.
    """

    def __init__(self, collada: Collada, resolution: int):
        self._collada = collada
        self._scene = collada.scene
        self.resolution = resolution
        self.camera = self.load_camera()
        self.objects = self.load_objects()
        self.lights = self.load_lights()
        self.materials = self.load_materials()

    def load_camera(self) -> Camera:
        """
        Load camera from scene
        """
        cameras = list(self._scene.objects("camera"))
        if len(cameras) != 1:
            raise Exception(
                "Invalid amount of cameras in the image, use one for gods sake!"
            )

        camera = cameras[0]
        return Camera(camera, self.resolution)

    def load_objects(self) -> List[Object]:
        """
        Load all objects from the scene
        """
        objects = list(self._scene.objects("geometry"))
        return [Object(g) for g in objects]

    def load_materials(self) -> Dict:
        """
        Load all objects from the scene
        """
        return {x.id: Material(x) for x in self._collada.materials}

    def get_material(self, id_) -> Any:
        """
        Get material by name
        """
        return self.materials[id_]

    def load_lights(self) -> Any:  # TODO
        """
        Load all lights
        """
        lights = list(self._scene.objects("light"))
        return lights

    @classmethod
    def load(self, path: str, resolution: int) -> "Scene":
        """
        Load scene
        """
        scene = Scene(Collada(path), resolution)
        return scene
