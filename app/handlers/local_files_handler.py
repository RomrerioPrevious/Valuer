from icecream import ic
from app import Logger
from app.config import Config
from app.models import TableFabric
import os


class LocalFilesHandler:
    def __init__(self):
        self.config = Config()
        self.path = self.config["entry-point"]["input"]

    def get_local_estimate_by_name(self, name: str) -> dict:
        file_name = self.find_estimate(name)
        table = TableFabric.fabric(self.path + file_name)
        workload, cost = self.find_fields(table, name)
        return {
            "workload": workload,
            "cost": cost
        }

    def find_fields(self, table, name) -> (float, float):
        workload = self.get_field(table, "workload")
        cost = self.get_field(table, "cost")
        if str(workload) == "nan" or str(cost) == "nan":
            workload, cost = self._find_fields_in_estimates(table, name)
        elif type(workload) != float or type(cost) != float:
            workload, cost = self._find_fields_in_estimates(table, name)
        return float(workload), float(cost)

    def _find_fields_in_estimates(self, table, name) -> (float, float):
        if not name:
            return 0, 0
        estiamtes = self.find_estimates(name)
        workload = 0.0
        cost = 0.0
        for file_name in estiamtes:
            try:
                temp_table = TableFabric.fabric(self.path + file_name)
                temp_workload, temp_cost = self.find_fields(temp_table, None)
                workload += temp_workload
                cost += temp_cost
            except FileNotFoundError:
                Logger.write_file_not_found(name)
        if workload and cost:
            return workload, cost
        for row_index in range(len(table) - 1):
            row = self.read_row(table, row_index)
            for file_name in row:
                if "Итого" in str(file_name):
                    return int(row[6]), int(row[7])
        return 0, 0

    def get_field(self, table, name: str):
        column = int(self.config["local-files-fields"][f"{name}_column"])
        row = int(self.config["local-files-fields"][f"{name}_row"])
        return table[column][row]

    @staticmethod
    def read_row(table, row_index) -> list:
        row = []
        for column in table.values():
            row.append(column[row_index])
        return row

    def find_estimate(self, name: str) -> str:
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_name = os.path.splitext(file)[0]
                if name in file_name:
                    return file
        raise FileNotFoundError(f"Not found file with name {name}")

    def find_estimates(self, name: str) -> [str]:
        result = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                file_name = os.path.splitext(file)[0]
                if name in file_name:
                    result.append(file)
        if len(result) == 0:
            raise FileNotFoundError(f"Not found file with name {name}")
        return result
