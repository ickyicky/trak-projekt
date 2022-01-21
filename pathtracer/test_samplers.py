#!/bin/python3

if __name__ == "__main__":
    from .samplers import AVAILABLE_SAMPLERS, Configuration, Sampler, sampler_factory
    import argparse
    import matplotlib.pyplot as plt
    from mpl_toolkits import mplot3d
    import numpy as np


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--algorithm", "-a", choices=AVAILABLE_SAMPLERS.keys(), help="Sampling algorithm", 
        type=str, action="store", default="random"
    )
    parser.add_argument(
        "--max-depth", "-d", help="Max depth", type=int, action="store", default=2
    )
    parser.add_argument(
        "--samples", "-s", help="Samples per pixel", type=int, action="store", default=1000
    )

    args = parser.parse_args()

    conf = Configuration(algorithm=args.algorithm, samples=args.samples, max_depth=args.max_depth)
    print(conf)
    sampler = sampler_factory(conf)
    data = sampler.all()

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x = data[:, 0]
    y = data[:, 1]
    z = data[:, 2]
    ax.scatter3D(x, y, z)

    plt.show()

