from unittest import TestCase
from icecream import ic
from app import Logger
from valuer import ValuerApp


class ViewTest(TestCase):
    def test_action(self):
        app.on_directory_tree_file_selected()
