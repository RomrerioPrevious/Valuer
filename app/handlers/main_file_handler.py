import os
from app.models import Table
from app.config import Config
from icecream import ic


class MainFileHandler:
    def __init__(self):
        config = Config()
        path = config["entry-point"]["main-file"]
        self.table = Table(path)
        self.fields = config["main-file-fields"]

    def parse(self):
        ...
