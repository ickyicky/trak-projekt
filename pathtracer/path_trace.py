from .procedure import MainProcedure
from .ray import Ray
from .collision import get_collision
from .bitmap import color, Bitmap
from .samplers import sampler_factory, Sampler
from .utils import print_progress_bar

from multiprocessing import Pool
import numpy as np
import os
from typing import List, Tuple


PROCESS_PROCEDURE = None


def hemisphere_mapping(point: np.array, normal: np.array) -> np.array:
    if np.dot(point, normal) < 0:
        return -point
    else:
        return point


def path_trace(procedure: MainProcedure) -> Bitmap:
    """
    Main procedure:

    creates bitmap, renders each pixel from corresponding
    ray generated by camera.
    """
    procedure.load_scene()
    procedure.scene.load_camera()
    bitmap = Bitmap(*procedure.scene.camera.resolution)

    pool = Pool(os.cpu_count())
    tasks = {}
    rays = procedure.scene.camera.generate_initial_rays()
    procedure.free_scene()  # for pickle

    for (x, y), ray in rays:
        tasks[(x, y)] = pool.apply_async(trace_ray_task, (ray, procedure))

    pool.close()
    pool.join()
    total = len(tasks)

    for i, (x, y) in enumerate(tasks.keys()):
        bitmap[y, x] = tasks[(x, y)].get()
        print_progress_bar(
            iteration=i,
            total=total,
            prefix="Rendering image...",
        )

    return bitmap


def trace_ray_task(
    ray: Ray,
    procedure_template: MainProcedure,
):
    """
    Task executed in Pool.
    """
    global PROCESS_PROCEDURE

    if PROCESS_PROCEDURE is None:
        PROCESS_PROCEDURE = procedure_template
        PROCESS_PROCEDURE.load_scene()
        PROCESS_PROCEDURE.load_background()
        PROCESS_PROCEDURE.scene.load_objects()
        PROCESS_PROCEDURE.scene.load_materials()

    samples = PROCESS_PROCEDURE.config.samples
    result = np.array([0.0, 0.0, 0.0])

    sampler = sampler_factory(PROCESS_PROCEDURE.config)

    for _ in range(samples):
        result += trace_ray(PROCESS_PROCEDURE, ray, sampler)

    result = (result / samples * 255).astype("uint8")
    return result


def trace_ray(
    procedure: MainProcedure,
    ray: Ray,
    sampler: Sampler,
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
        direction=hemisphere_mapping(next(sampler), hit.normal),
    )

    probability = 1 / (2 * np.pi)

    hit_material = procedure.scene.get_material(hit.material_id)

    emmitance = hit_material.emmitance

    cos_theta = np.dot(new_ray.direction, hit.normal)

    brdf = (hit_material.diffusion * cos_theta) + (  # diffusion brdf
        hit_material.reflectance
        * (np.dot(ray.direction, new_ray.direction) ** hit_material.shiness)
    )  # reflectance brdf

    incoming = trace_ray(procedure, new_ray, sampler, depth + 1)

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
    return procedure.background(ray)
