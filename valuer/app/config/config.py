from configparser import ConfigParser
import os
import ast


class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            parser = ConfigParser()
            dir_path = Config.find_config_path()
            parser.read(dir_path, encoding="UTF-8")
            config = {}
            for section in parser.sections():
                config[section] = dict(parser.items(section))
            config["file"]["local-file"] = ast.literal_eval(config["file"]["local-file"])
            cls.instance = config
        return cls.instance

    @staticmethod
    def find_config_path():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.removesuffix("app\\config")
        dir_path += "resources\\config.ini"
        return dir_path

    @staticmethod
    def find_global_path():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.removesuffix("app\\config")
        return dir_path
