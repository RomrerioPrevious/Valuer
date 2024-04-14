from icecream import ic
from app.config import Config
import pandas as pd


class MainFileHandler:
    def __init__(self):
        config = Config()
        path = config["entry-point"]["main-file"]
        self.table = pd.read_excel(path)  # TODO create xml read
        self.fields = config["main-file-fields"]
