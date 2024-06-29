from textual.app import ComposeResult
from textual.widgets import Static, DataTable
from icecream import ic


class Table(DataTable):
    @staticmethod
    def create_row(i: int, table: dict) -> tuple:
        row = []
        for column in table.values():
            if str(column[i]) == "nan":
                row.append("-")
            else:
                cell = str(column[i])
                if len(cell) >= 15:
                    cell = f"{cell[0:15]}..."
                row.append(cell)
        return tuple(row)

    @staticmethod
    def create_header(table: dict) -> tuple:
        row = []
        for column in table.keys():
            if str(column)[0:9] == "Unnamed: ":
                row.append("-")
            else:
                cell = str(column)
                if len(cell) >= 15:
                    cell = f"{cell[0:15]}..."
                row.append(cell)
        return tuple(row)
