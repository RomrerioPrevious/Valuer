from pathlib import Path
from typing import Iterable
from textual.widgets import DirectoryTree


class FileTree(DirectoryTree):
    directory = "./"

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]

    def set_directory(self, directory: str):
        self.directory = directory
