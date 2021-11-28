if __name__ == "__main__":
    import argparse

    from .samplers import Samplers
    from .procedure import MainProcedure

    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Scene file")
    parser.add_argument("algorithm", choices=Samplers.keys(), help="Sampling algorithm")
    parser.add_argument("environment", help="Environment map")

    args = parser.parse_args()
    MainProcedure(
        scene_file=args.scene,
        sampler_cls=Samplers[args.algorithm],
        environment_map=args.environment,
    ).render()
