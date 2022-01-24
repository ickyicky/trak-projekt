if __name__ == "__main__":
    import argparse

    from .samplers import AVAILABLE_SAMPLERS, Configuration
    from .procedure import MainProcedure
    from .bitmap import color

    def color_type(arg_value):
        try:
            R, G, B = [int(x) for x in arg_value.split(",")]
            return color(R, G, B) / 255
        except TypeError:
            raise argparse.ArgumentTypeError

    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Scene file")
    parser.add_argument(
        "algorithm", choices=AVAILABLE_SAMPLERS.keys(), help="Sampling algorithm"
    )
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--map", "-m", action="store", help="Cyllindric environment map file"
    )
    group.add_argument(
        "--color",
        "-c",
        action="store",
        help="Background color as string in format R,G,B",
        type=color_type,
    )

    args = parser.parse_args()

    config = Configuration(
        algorithm=args.algorithm,
        max_depth=args.max_depth,
        samples=args.samples,
        background_color=args.color,
        environment_map=args.map,
    )

    MainProcedure(
        config=config,
        scene_file=args.scene,
        resolution=args.resolution,
    ).render(args.output)
