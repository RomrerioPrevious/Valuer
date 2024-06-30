from unittest import TestCase
from valuer.app import Config


class ConfigTest(TestCase):
    config = Config()

    def test_get(self):
        theme = self.config["interface"]["theme"]
        assert theme == "dark"
