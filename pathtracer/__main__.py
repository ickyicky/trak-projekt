if __name__ == "__main__":
    import argparse

    from .samplers import Samplers
    from .procedure import MainProcedure

    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Scene file")
    parser.add_argument("algorithm", choices=Samplers.keys(), help="Sampling algorithm")
    parser.add_argument("environment", help="Environment map")
    parser.add_argument("output", help="Output file")
    parser.add_argument(
        "resolution",
        help="Vertical resolution, for example 720 for 720p. Keep in mind that aspect ratio is definied by camera.",
        type=int,
    )

    args = parser.parse_args()
    MainProcedure(
        scene_file=args.scene,
        resolution=args.resolution,
        sampler_cls=Samplers[args.algorithm],
        environment_map=args.environment,
    ).render(args.output)
