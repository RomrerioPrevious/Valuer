import os
from icecream import ic
from os import path
import pandas as pd


class Table:
    def __init__(self, path: str):
        extention = os.path.splitext(path)[1]
        match extention:
            case ".xml":
                ...
            case _:
                self.table = pd.read_excel(path)

    def __getitem__(self, item: (int, int)):
        ...
