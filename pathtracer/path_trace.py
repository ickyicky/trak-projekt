from .procedure import MainProcedure
from .ray import Ray


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
):
    """
    Trace ray, pseudocode
    """
    if depth > procedure.config.max_depth:
        return background(procedure, ray)

    hit = get_collision(ray, procedure)

    if hit is None:
        return background(procedure, ray)

    reflected_ray = procedure.sampler(ray, hit)
    value = trace_ray(procedure, reflected_ray, depth + 1)
    return hit.object.value + value * brdf


def background(
    procedure: MainProcedure,
    ray: Ray,
):
    """
    Gets environment map value for the ray
    """
    pass
