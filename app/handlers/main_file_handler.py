import os
from .local_files_handler import LocalFilesHandler
from app.models import TableFabric, Estimate
from app.config import Config, Logger
from app.models.result import Result
from icecream import ic


class MainFileHandler:
    def __init__(self):
        config = Config()
        path = config["entry-point"]["main-file"]
        self.config = config
        self.table = TableFabric.fabric(path)
        self.fields = config["main-file-fields"]

    def parse(self):
        row_index = int(self.fields["start-row"])
        end_row = len(self.table[0])
        estimates = []
        result_name = ""
        while row_index != end_row:
            row = self.read_row(row_index)
            if self.is_result(row):
                result = self.create_result(estimates, result_name)
                self.save_result(result)
                estimates = []
                result_name = ""
            elif not result_name:
                result_name = self.find_name(row)
            else:
                estimate = self.create_estimate(row)
                estimates.append(estimate)
            row_index += 1

    def create_result(self, estimates: [Estimate], name: str) -> Result:
        result = Result.create_with_name(name)
        handler = LocalFilesHandler()
        for i in estimates:
            try:
                local_estimate = handler.get_local_estimate_by_name(i.name)
                i.workload = local_estimate["workload"]
                if not i.cost:
                    i.cost = local_estimate["cost"]
            except FileNotFoundError:
                Logger.write_file_not_found(i.name)
            except BaseException as err:
                Logger.write_error(err)
            finally:
                result.global_workload += i.workload
                result.global_cost += i.cost
                result.estimates.append(i)
        ic(result)
        return result

    def save_result(self, result: Result) -> None:
        output = self.config["entry-point"]["output"]

    def find_name(self, row: list) -> str:
        for i in row:
            if i:
                return i

    def create_estimate(self, row: list) -> Estimate:
        name = row[int(self.fields["name"])]
        cost = row[int(self.fields["cost"])]
        return Estimate(
            name=name,
            workload=0,
            cost=cost
        )

    def read_row(self, row_index: int) -> list:
        row = []
        for column in self.table.values():
            row.append(column[row_index])
        return row

    def is_result(self, row: list) -> bool:
        for i in row:
            if "Итого" in str(i):
                return True
        return False
