import yaml


def read_config() -> dict:
    with open('../settings.yaml', ) as f:
        cfg = yaml.load(f, Loader=yaml.CLoader)
        return cfg
