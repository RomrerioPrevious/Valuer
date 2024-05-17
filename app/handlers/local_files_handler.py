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
        self.local = self.config["local-files-fields"]

    def get_local_estimate_by_name(self, name: str) -> [SubEstimate]:
        estimates_files = self.find_estimates(name)
        sub_estimates = None
        for file_name in estimates_files:
            try:
                temp_table = TableFabric.fabric(self.path + file_name)
                sub_estimates = self.find_sub_estimates(temp_table)
            except FileNotFoundError:
                Logger.write_file_not_found(file_name)
        return sub_estimates

    def find_sub_estimates(self, table: dict) -> [SubEstimate]:
        start = int(self.local["start-row"])
        estimates = {}
        for i in range(start, len(table[0])):
            try:
                row = self.read_row(table, i)
                sub_estimate = SubEstimate(
                    name=row[int(self.local["name"])],
                    unit=row[int(self.local["unit"])],
                    quantity=row[int(self.local["quantity"])],
                    cost_of_quantity=row[int(self.local["cost_of_quantity"])]
                )
                if str(sub_estimate.unit) == "nan":
                    continue
                if sub_estimate.unit in estimates:
                    temp = estimates[sub_estimate.unit]
                    temp.quantity += sub_estimate.quantity
                    temp.cost_of_quantity += sub_estimate.cost_of_quantity
                else:
                    estimates[sub_estimate.unit] = sub_estimate
            except BaseException as err:
                Logger.write_error(err)
        return estimates.values()

    @staticmethod
    def read_row(table, row_index) -> list:
        row = []
        for column in table.values():
            row.append(column[row_index])
        return row

    def find_estimates(self, name: str) -> [str]:
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
