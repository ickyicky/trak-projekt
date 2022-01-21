if __name__ == "__main__":
    import argparse

    from .samplers import AVAILABLE_SAMPLERS, Configuration
    from .procedure import MainProcedure

    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Scene file")
    parser.add_argument(
        "algorithm", choices=AVAILABLE_SAMPLERS.keys(), help="Sampling algorithm"
    )
    parser.add_argument("environment", help="Environment map")
    parser.add_argument("output", help="Output file")
    parser.add_argument(
        "resolution",
        help="Vertical resolution, for example 720 for 720p. Keep in mind that aspect ratio is definied by camera.",
        type=int,
    )
    parser.add_argument(
        "--max-depth", "-d", help="Max depth", type=int, action="store", default=2
    )
    parser.add_argument(
        "--samples", "-s", help="Samples per pixel", type=int, action="store", default=2
    )

    args = parser.parse_args()

    MainProcedure(
        config=Configuration(algorithm=args.algorithm, max_depth=args.max_depth, samples=args.samples),
        scene_file=args.scene,
        resolution=args.resolution,
        environment_map=args.environment,
    ).render(args.output)
