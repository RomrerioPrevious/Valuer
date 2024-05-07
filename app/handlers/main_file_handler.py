import os
from .local_files_handler import LocalFilesHandler
from app.models import TableFabric, Estimate
from app.config import Config
from icecream import ic

from ..models.result import Result


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
        while row_index != end_row:
            row = self.read_row(row_index)
            if self.is_result(row):
                result = self.create_result(estimates)
                self.save_result(result)
            else:
                estimate = self.create_estimate(row)
                estimates.append(estimate)
            row_index += 1

    def create_result(self, estimates: [Estimate]) -> Result:
        result = Result.create_empty()
        handler = LocalFilesHandler()
        for i in estimates:
            local = handler.find_local_estimate(i.name)
            i.workload = local["workload"]
            i.cost = local["cost"]
            result.estimates.append(i)
        return result

    def save_result(self, result: Result) -> None:
        output = self.config["entry-point"]["output"]

    def create_estimate(self, row: list) -> Estimate:
        name = row[int(self.fields["name"])]
        unit = row[int(self.fields["unit"])]
        scope_of_work = row[int(self.fields["scope-of-work"])]
        cost = row[int(self.fields["cost"])]
        return Estimate(
            name=name,
            unit=unit,
            workload=scope_of_work,
            cost=cost
        )

    def read_row(self, row_index: int) -> list:
        row = []
        for column in self.table:
            row.count(column[row_index])
        return row

    def is_result(self, row: list) -> bool:
        ...
