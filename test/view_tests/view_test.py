from unittest import TestCase


class ViewTest(TestCase):
    def test_action(self):
        app.on_directory_tree_file_selected()
