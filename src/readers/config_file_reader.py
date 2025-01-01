import yaml


class ConfigFileReader:
    def read(self, file_path):
        with open(file_path, "r") as f:
            loaded = yaml.load(f, Loader=yaml.CLoader)
            return loaded
