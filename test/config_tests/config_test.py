from unittest import TestCase
from app.config import Config
import pytest


class ConfigTest(TestCase):
    config = Config()

    def test_get(self):
        theme = self.config["interface"]["theme"]
        assert theme == "dark"
