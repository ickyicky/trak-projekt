from .procedure import MainProcedure
from .ray import Ray
from .object import Object
from dataclasses import dataclass
import numpy as np


@dataclass
class Hit:
    coords: np.array
    hit_object: Object


def get_collision(
    procedure: MainProcedure,
    ray: Ray,
) -> Hit:
    """
    Calculates collision for given ray
    on procedures scene
    """
    pass
