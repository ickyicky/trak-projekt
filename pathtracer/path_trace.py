from .procedure import MainProcedure
from .ray import Ray
from .collision import get_collision
from .bitmap import Color

import numpy as np


def path_trace(procedure: MainProcedure) -> None:
    """
    Procedure stores render configuration

    Pseudocode
    """
    for ray in procedure.scene.camera.generate_initial_rays():
        trace_ray(procedure, ray)


def trace_ray(
    procedure: MainProcedure,
    ray: Ray,
    depth: int = 0,
) -> Color:
    """
    Trace ray, pseudocode
    """
    if depth > procedure.config.max_depth:
        return background(procedure, ray)

    hit = get_collision(ray, procedure)

    if hit is None:
        return background(procedure, ray)

    reflected_ray = Ray(
        origin=hit.coords,
        direction=sampler_in_hemisphere(hit.normal),
    )
    value = trace_ray(procedure, reflected_ray, depth + 1)
    return hit.hit_object.value + value * brdf


def sampler_in_hemisphere(
    normal: np.array,
) -> np.array:
    """
    Generates random direction for new
    ray
    """
    pass


def background(
    procedure: MainProcedure,
    ray: Ray,
) -> Color:
    """
    Gets environment map value for the ray
    or returns black other way
    """
    return Color(0, 0, 0)
