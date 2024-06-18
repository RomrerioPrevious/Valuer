import os
from icecream import ic
from os import path
import xml.etree.ElementTree as ET
import pandas as pd
from app import Logger


class TableFabric:
    @staticmethod
    def fabric(path: str) -> dict:
        extention = os.path.splitext(path)[1]
        table = None
        match extention:
            case ".xml":
                table = TableFabric.read_xml(path)
            case ".xlsx":
                table = pd.read_excel(path).to_dict()
            case ".xls":
                table = pd.read_excel(path).to_dict()
            case _:
                Logger.write_error(f"Uncorrect extention {extention}")
        table = TableFabric.rename_tabel_columns(table)
        return table

    @staticmethod
    def read_xml(file: str):
        tree = ET.parse(file)
        root = tree.getroot()

        def parse_element(element):
            result = {}
            for child in element:
                if len(child) == 0:
                    result[child.tag] = child.text
                else:
                    result[child.tag] = parse_element(child)
        return {root.tag: parse_element(root)}

    @staticmethod
    def rename_tabel_columns(table: dict) -> dict:
        new_table = {}
        for i, column in enumerate(table.values()):
            new_table[i] = column
            del column
        return new_table
