from unittest import TestCase
from icecream import ic
from app import Logger
from app.handlers import MainFileHandler
import pytest
from app.models import Estimate


class MainHandlerTest(TestCase):
    handler = MainFileHandler()
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
            workload=0,
        )
        row = self.handler.read_row(30)
        estimate = self.handler.create_estimate(row)
        assert estimate.name == correct.name and estimate.cost == correct.cost

    def test_parse(self):
        self.handler.parse()
