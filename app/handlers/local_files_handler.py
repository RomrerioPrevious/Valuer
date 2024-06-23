from icecream import ic
from app import Logger
from app.config import Config
from app.models import TableFabric, Estimate
import os

from app.models.sub_estimate import SubEstimate


class LocalFilesHandler:
    def __init__(self):
        self.config = Config()
        self.path = self.config["entry-point"]["input"]
        self.config_of_local = self.config["file"]["local-file"]

    def parse_local_estimate(self, name: str) -> [SubEstimate]:
        estimates_files = self.find_files(name)
        sub_estimates = []
        for file_name in estimates_files:
            try:
                temp_table = TableFabric.fabric(self.path + file_name)
                sub = self.parse_file(temp_table)
                if not sub:
                    continue
                for i in sub:
                    sub_estimates.append(i)
            except FileNotFoundError:
                Logger.write_file_not_found(file_name)
        return sub_estimates

    def find_files(self, name: str) -> [str]:
        result = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_name = os.path.splitext(file)[0]
                for i in range(len(name)):
                    if file_name[i] != name[i]:
                        break
                else:
                    result.append(file)
        if len(result) == 0:
            raise FileNotFoundError(f"Not found file with name {name}")
        return result

    def parse_file(self, table: dict) -> [SubEstimate]:
        for variation in range(len(self.config_of_local)):
            sub_estimates = self.parse_file_with_variations(table, variation)
            if sub_estimates:
                return sub_estimates
        raise ValueError(f"Couldn't analyze the estimate.")  # TODO normal errors

    def parse_file_with_variations(self, table: dict, variation: int) -> [SubEstimate]:
        local = self.config_of_local[variation]
        start = int(local["start-row"])
        estimates = []
        for i in range(start, len(table[0])):
            try:
                row = self.read_row(table, i)
                cost_index = int(local["cost"])
                cost_of_quantity_index = int(local["cost_of_quantity"])
                if str(row[cost_index]) == "nan":
                    next_row = self.read_row(table, i + 1)
                    cost = next_row[cost_index]
                    cost_of_quantity = next_row[cost_of_quantity_index]
                else:
                    cost = row[cost_index]
                    cost_of_quantity = row[cost_of_quantity_index]
                sub_estimate = SubEstimate(
                    name=row[int(local["name"])],
                    unit=row[int(local["unit"])],
                    quantity=row[int(local["quantity"])],
                    cost_of_quantity=cost_of_quantity,
                    cost=cost
                )
                if not sub_estimate.is_full_estimate():
                    continue
                estimates.append(sub_estimate)
            except BaseException as err:
                Logger.write_error(err)
        return estimates

    @staticmethod
    def read_row(table, row_index) -> list:
        row = []
        for column in table.values():
            row.append(column[row_index])
        return row
