import os
import pandas as pd


class TableFabric:
    @staticmethod
    def fabric(path: str) -> dict:
        extension = os.path.splitext(path)[1]
        match extension:
            case ".xml":
                table = pd.read_xml(path, encoding="UTF-8").to_dict()
            case ".xlsx" | ".ods" | ".xls":
                table = pd.read_excel(path, engine="openpyxl").to_dict()
            case ".csv":
                table = pd.read_csv(path, encoding="UTF-8").to_dict()
            case _:
                raise PermissionError(f"Incorrect extension {extension}")
        table = TableFabric.rename_tabel_columns(table)
        return table

    @staticmethod
    def rename_tabel_columns(table: dict) -> dict:
        new_table = {}
        for i, column in enumerate(table.values()):
            new_table[i] = column
            del column
        return new_table

    @staticmethod
    def fabric_without_rename(path: str) -> dict:
        extension = os.path.splitext(path)[1]
        match extension:
            case ".xml":
                table = pd.read_xml(path).to_dict()
            case ".xlsx" | ".ods" | ".xls":
                table = pd.read_excel(path).to_dict()
            case ".csv":
                table = pd.read_csv(path).to_dict()
            case _:
                raise PermissionError(f"Incorrect extension {extension}")
        return table
