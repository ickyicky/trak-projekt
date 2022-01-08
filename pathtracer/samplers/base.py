from contextlib import contextmanager
import numpy as np
from .random import RandomSampler


IMPLEMENTATION = None


AVALIBE_SAMPLERS = {
    "random": RandomSampler,
    "stratified": None,
    "multijittered": None,
    "low-discrepancy_series": None,
}


def configure(sampler_name, config):
    """
    Configures global sampler
    for even distribution
    """
    global IMPLEMENTATION

    assert sampler_name in AVALIBE_SAMPLERS, "invalid sampler name"

    sampler_cls = AVALIBE_SAMPLERS[sampler_name]

    if IMPLEMENTATION is not None:
        raise Exception("trying to configure already configured sampler!")

    IMPLEMENTATION = sampler_cls(**config)


@contextmanager
def get_implementation():
    """
    Wrapper around getting global implementation
    and checking if it is configured, hence not None
    """
    global IMPLEMENTATION
    assert IMPLEMENTATION is not None, "configure samplers first"
    yield IMPLEMENTATION


def sampler_in_hemisphere(
    normal: np.array,
) -> np.array:
    """
    Generates random direction for new
    ray
    """
    result = None

    with get_implementation() as impl:
        result = impl(normal)

    return result
