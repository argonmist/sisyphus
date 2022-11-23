import yaml
import os

def read(yaml_file):
    home = os.getenv('HOME')
    basic_path = home + '/sisyphus/yamls/'
    full_path = basic_path + yaml_file
    with open(full_path, "r") as stream:
        try:
            settings = yaml.safe_load(stream)
            return settings
        except yaml.YAMLError as exc:
            print(exc)
