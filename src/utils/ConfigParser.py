import yaml

configs_path = "configs/test_configs.yaml"

class ConfigParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}

    def parse(self):
        with open(self.config_file, "r") as f:
            loaded = yaml.load(f, Loader=yaml.CLoader)
            self.config = loaded