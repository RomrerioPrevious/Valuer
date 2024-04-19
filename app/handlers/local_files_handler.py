from icecream import ic
from app.config import Config
import pandas as pd


class LocalFilesHandler:
    def __init__(self):
        config = Config()
        path = config["entry-point"]["input"]

    def find_local_estimate(self):
        ...
