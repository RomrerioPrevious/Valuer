from pathlib import Path
from typing import Iterable
from textual.app import ComposeResult
from textual.widgets import Static, DirectoryTree, Tree
from icecream import ic
from textual.widgets._directory_tree import DirEntry


class FileTree(DirectoryTree):
    directory = "./"

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        return [path for path in paths if not path.name.startswith(".")]

    def set_directory(self, directory: str):
        self.directory = directory
