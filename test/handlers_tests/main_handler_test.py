from unittest import TestCase
from app.handlers import MainFileHandler
import pytest


class MainHandlerTest(TestCase):
    handler = MainFileHandler()

    def test_read(self):
        table = self.handler.table
        column = table["Unnamed: 1"]
        row = column[31]
        assert 'Итого по Главе 1. "Подготовка территории строительства"' == row
