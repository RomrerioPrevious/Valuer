from configparser import ConfigParser
import ast


class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            parser = ConfigParser()
            parser.read("D:/Save/Valuer/config.ini", encoding="UTF-8")  # TODO normal path (config.ini)
            config = {}
            for section in parser.sections():
                config[section] = dict(parser.items(section))
            config["file"]["local-file"] = ast.literal_eval(config["file"]["local-file"])
            cls.instance = config
        return cls.instance
