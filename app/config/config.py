from configparser import ConfigParser
from icecream import ic


class Config(ConfigParser):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            parser = ConfigParser()
            parser.read("D:/Save/Valuer/resources/config.ini", encoding="UTF-8")
            cls.instance = parser
        return cls.instance
