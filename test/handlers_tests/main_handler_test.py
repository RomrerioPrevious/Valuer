from unittest import TestCase
from icecream import ic
from app import Logger
from app.handlers import FileHandler
import pytest
from app.models import Estimate
from app.models.result import Result
from app.models.sub_estimate import SubEstimate


class MainHandlerTest(TestCase):
    handler = FileHandler()
    ic.configureOutput(prefix=Logger.info,
                       outputFunction=Logger.write_log)
    Logger.clear_fnf()
    Logger.clear()

    def test_read(self):
        table = self.handler.table
        column = table[1]
        row = column[31]
        assert 'Итого по Главе 1. "Подготовка территории строительства"' == row

    def test_create_estimate(self):
        correct = Estimate(
            name="Смета. Договор № 583-СТУ/21, прил. 4",
            cost=408,
            sub_estimates=[],
        )
        row = self.handler.read_row(30)
        estimate = self.handler.create_estimate(row)
        assert estimate.name == correct.name and estimate.cost == correct.cost

    def test_save_result(self):
        result = Result(name="test",
                        global_cost=1000,
                        estimates=[
                            Estimate(
                                name="1",
                                cost=1000.0,
                                sub_estimates=[
                                    SubEstimate(
                                        name="gg",
                                        unit="m",
                                        quantity=20.0,
                                        cost_of_quantity=1000.0
                                    )
                                ]
                            )
                        ])
        self.handler.save_result(result, 1)

    def test_parse(self):
        self.handler.parse()
