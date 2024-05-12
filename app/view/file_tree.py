from textual.app import ComposeResult
from textual.widgets import Static, DirectoryTree
from icecream import ic


class FileTree(Static):
    directory = "./"

    def compose(self) -> ComposeResult:
        yield DirectoryTree(self.directory)

    def set_directory(self, directory: str):
        self.directory = directory
