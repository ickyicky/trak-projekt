from .procedure import MainProcedure
from .ray import Ray
from dataclasses import dataclass
import numpy as np
from typing import Any


@dataclass
class Hit:
    coords: np.array
    hit_object: Any


def get_collision(
    ray: Ray,
    procedure: MainProcedure,
) -> Hit:
    """
    Calculates collision for given ray
    on procedures scene
    """
    hit_primitive = None
    hit_t = None
    hit_v = None

    for obj in procedure.scene.objects:
        for primitive in obj.primitives:
            for i in range(len(primitive)):
                triangle = primitive[i]
                hits, vals = intersect(ray, triangle)
                if hits and vals[0] < hit_t:
                    hit_t = vals[0]
                    hit_v = vals[2]
                    hit_primitive = primitive

    return Hit(hit_v, hit_primitive)


def intersect(ray: Ray, triangle) -> int:
    """
    Calculates if ray will hit the triangle
    """
    null_inter = np.array([np.nan, np.nan, np.nan])

    # break down triangle into the individual points
    v1, v2, v3 = triangle.vertices
    eps = 0.000001

    # compute edges
    edge1 = v2 - v1
    edge2 = v3 - v1
    pvec = np.cross(ray.direction, edge2)
    det = edge1.dot(pvec)

    if abs(det) < eps:  # no intersection
        return False, null_inter
    inv_det = 1.0 / det
    tvec = ray.origin - v1
    u = tvec.dot(pvec) * inv_det

    if u < 0.0 or u > 1.0:  # if not intersection
        return False, null_inter

    qvec = np.cross(tvec, edge1)
    v = ray.direction.dot(qvec) * inv_det
    if v < 0.0 or u + v > 1.0:  # if not intersection
        return False, null_inter

    t = edge2.dot(qvec) * inv_det
    if t < eps:
        return False, null_inter

    return True, np.array([t, u, v])
