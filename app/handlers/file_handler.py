from .local_files_handler import LocalFilesHandler
from app.models import TableFabric, Estimate
from app.config import Config, Logger
from app.models.result import Result
import pandas as pd
from icecream import ic

from ..models.sub_estimate import SubEstimate


class FileHandler:
    def __init__(self):
        config = Config()
        path = config["entry-point"]["main-file"]
        self.config = config
        self.table = TableFabric.fabric(path)
        self.fields = config["file"]
        self.number = 1

    def parse(self):
        end_row = self.get_end_row()
        estimates = []
        name = ""
        for row_index in range(int(self.fields["start-row"]), end_row):
            row = self.read_row(row_index)
            if self.is_result(row):
                result = self.create_result(estimates, name)
                self.save_result(result)
                estimates = []
                name = ""
                self.number += 1
            elif not name:
                name = self.find_name(row)
            else:
                estimate = self.create_estimate(row)
                estimates.append(estimate)

    def get_end_row(self):
        end_row = self.fields["end-row"]
        if not end_row:
            end_row = len(self.table[0])
        else:
            end_row = int(end_row)
        return end_row

    def read_row(self, row_index: int) -> list:
        row = []
        for column in self.table.values():
            row.append(column[row_index])
        return row

    def create_estimate(self, row: list) -> Estimate:
        estimate = Estimate.create_empty()
        estimate.name = row[int(self.fields["name"])]
        estimate.cost = row[int(self.fields["cost"])]
        return estimate

    @staticmethod
    def create_result(estimates: [Estimate], name: str) -> Result:
        result = Result.create_with_name(name)
        handler = LocalFilesHandler()
        for i in estimates:
            try:
                local_estimates = handler.parse_local_estimate(i.name)
                i.sub_estimates = local_estimates
            except FileNotFoundError:
                Logger.write_file_not_found(i.name)
            except BaseException as err:
                Logger.write_error(err)
            finally:
                result.global_cost += i.cost
                result.estimates.append(i)
        ic(result)
        return result

    def save_result(self, result: Result) -> None:
        output = self.config["entry-point"]["output"]
        header = False
        if self.number == 1:
            header = True
        data = self.create_data(result)
        frame = pd.DataFrame(data=data)
        frame.to_csv(output, mode="a", index=True, header=header)

    def create_data(self, result: Result) -> dict:
        data = {
            "Номера позиций в лс (сметах) для суммы": {},
            "Наименование конструктивных решений (элементов), комплексов (видов) работ": {},
            "Единица измерения": {},
            "Количество (объем работ)": {},
            "Цена на единицу измерения, без НДС, руб.": {},
            "Стоимость всего, руб.": {}
        }
        self.add_name_in_data(data, result.name)
        for i, estimate in enumerate(result.estimates):
            self.add_estimate_in_data(data, estimate, i)
        return data

    def add_estimate_in_data(self, data: dict, estimate: Estimate, num: int):
        if len(estimate.sub_estimates) == 1:
            number = f"{str(self.number)}.{num}"
            self.add_sub_estimate_in_data(data, estimate.sub_estimates[0], estimate.name, number)
        else:
            for i, sub in enumerate(estimate.sub_estimates):
                number = f"{str(self.number)}.{num}.{str(i)}"
                self.add_sub_estimate_in_data(data, sub, estimate.name, number)
        self.number += 1

    @staticmethod
    def add_sub_estimate_in_data(data: dict, sub: SubEstimate, ls: str, number: str):
        data["Номера позиций в лс (сметах) для суммы"][number] = ls
        data["Наименование конструктивных решений (элементов), комплексов (видов) работ"][number] = sub.name
        data["Единица измерения"][number] = sub.unit
        data["Количество (объем работ)"][number] = sub.quantity
        data["Цена на единицу измерения, без НДС, руб."][number] = sub.cost_of_quantity
        data["Стоимость всего, руб."][number] = sub.cost

    def add_name_in_data(self, data: dict, name: str):
        for i in data.keys():
            data[i][self.number] = ""
        data["Наименование конструктивных решений (элементов), комплексов (видов) работ"][self.number] = name

    @staticmethod
    def is_result(row: list) -> bool:
        for i in row:
            if "Итого" in str(i):
                return True
        return False

    @staticmethod
    def find_name(row: list) -> str:
        for i in row:
            if i:
                return i
