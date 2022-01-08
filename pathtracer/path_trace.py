from .procedure import MainProcedure
from .ray import Ray
from .collision import get_collision
from .bitmap import color, Bitmap
from .samplers import sampler_in_hemisphere

from multiprocessing import Pool
import numpy as np
import os


def path_trace(procedure: MainProcedure) -> Bitmap:
    """
    Main procedure:

    creates bitmap, renders each pixel from corresponding
    ray generated by camera.
    """
    bitmap = Bitmap(*procedure.scene.camera.resolution)

    pool = Pool(os.cpu_count())
    tasks = {}

    for (x, y), ray in procedure.scene.camera.generate_initial_rays():
        tasks[(x, y)] = pool.apply_async(
            trace_ray_task, (ray, procedure.scene_file, procedure.resolution)
        )

    for x, y in tasks.keys():
        bitmap[x, y] = tasks[(x, y)].get()

    return bitmap


def trace_ray_task(
    ray: Ray,
    scene_file: str,
    resolution: int,
):
    """
    Task executed in Pool
    """
    procedure = MainProcedure(scene_file, resolution, None)
    samples = procedure.config.samples
    result = np.array([0.0, 0.0, 0.0])

    for sample in range(samples):
        result += trace_ray(procedure, ray) / samples

    return result


def trace_ray(
    procedure: MainProcedure,
    ray: Ray,
    depth: int = 0,
) -> np.array:
    """
    Trace ray
    """
    if depth > procedure.config.max_depth:
        return background(procedure, ray)

    hit = get_collision(ray, procedure)

    if hit is None:
        return background(procedure, ray)

    new_ray = Ray(
        origin=hit.coords,
        direction=sampler_in_hemisphere(hit.normal),
    )

    probability = 1 / (2 * np.pi)

    hit_material = procedure.scene.get_material(hit.material_id)

    emmitance = hit_material.emmitance

    cos_theta = np.dot(new_ray.direction, hit.normal)
    brdf = hit_material.reflectance / np.pi

    incoming = trace_ray(procedure, new_ray, depth + 1)

    # RENDER EQUATION
    return emmitance + (incoming * brdf * cos_theta / probability)


def background(
    procedure: MainProcedure,
    ray: Ray,
) -> np.array:
    """
    Gets environment map value for the ray
    or returns black other way
    """
    return color(0, 0, 0)
