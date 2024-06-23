from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Header, Footer, Input, DirectoryTree, Button
from tkinter import filedialog
from app import Logger
from app.models import TableFabric
from app.view import *
from icecream import ic


class ValuerApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Theme"),
                ("ctrl+p", "open_path", "Open path")]
    CSS_PATH = "resources/style/index.tcss"

    def compose(self) -> ComposeResult:
        yield Header(name="Valuer")
        with Container():
            yield FileTree(id="file-tree-view", path="D://test//Сметы")
            with Vertical(id="code-view"):
                yield Table(id="table-view", show_header=False)
                with Container():
                    yield Input(id="what")
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        event.stop()
        table_view = self.query_one("#table-view", Table)
        table_view.clear()
        try:
            table = TableFabric.fabric(str(event.path))
            table_view.add_columns(*[i for i in range(0, len(table.keys()))])
            for i in range(0, len(table[0])):
                row = []
                for column in table.values():
                    if str(column[i]) == "nan":
                        row.append("-")
                    else:
                        cell = str(column[i])
                        if len(cell) >= 15:
                            cell = f"{cell[0:15]}..."
                        row.append(cell)
                table_view.add_row(*tuple(row))
        except PermissionError as ex:
            Logger.write_error(ex)

    def action_open_path(self):
        tree = self.query_one("#file-tree-view", FileTree)
        directory = filedialog.askdirectory()
        tree.path = directory

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
