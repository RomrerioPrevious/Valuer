import os
from icecream import ic
from os import path
import pandas as pd


class TableFabric:
    @staticmethod
    def fabric(path: str) -> dict:
        extention = os.path.splitext(path)[1]
        table = None
        match extention:
            case ".xml":
                ...
            case _:
                table = pd.read_excel(path).to_dict()
        table = TableFabric.rename_tabel_columns(table)
        return table

    @staticmethod
    def rename_tabel_columns(table: dict) -> dict:
        new_table = {}
        for i, column in enumerate(table.values()):
            new_table[i] = column
            del column
        return new_table
