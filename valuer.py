from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Header, Footer, Input, DirectoryTree, Button, TabbedContent, TabPane
from tkinter import filedialog
from app import Logger
from app.models import TableFabric
from app.view import *
from icecream import ic


class ValuerApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Theme"),
                ("ctrl+p", "open_path", "Open path"),
                ("ctrl+s", "start", "Start")]
    CSS_PATH = "resources/style/index.tcss"

    def compose(self) -> ComposeResult:
        yield Header(name="Valuer")
        with Container():
            yield FileTree(id="file-tree-view", path="D://test//Сметы")
            with Vertical(id="code-view"):
                yield Table(id="table-view", show_header=False)
                with TabbedContent(id="tabs"):
                    with TabPane("ССР"):
                        with Horizontal():
                            with Container():
                                yield Input(id="name", placeholder="name")
                                yield Input(id="start-row", placeholder="start row")
                                yield Input(id="file", placeholder="file path")
                            with Container():
                                yield Input(id="cost", placeholder="cost")
                                yield Input(id="end-row", placeholder="end row")
                                yield Input(id="output", placeholder="output file")
                    with TabPane("Variation 1"):
                        with Horizontal():
                            with Container():
                                yield Input(id="name-var1", placeholder="name")
                                yield Input(id="quantity-var1", placeholder="quantity")
                                yield Input(id="start-row-var1", placeholder="start row")
                            with Container():
                                yield Input(id="unit-var1", placeholder="unit")
                                yield Input(id="cost_of_quantity-var1", placeholder="cost of quantity")
                                yield Input(id="cost-var1", placeholder="cost")
                    with TabPane("+"):
                        ...
        yield Footer()

    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        event.stop()
        table_view = self.query_one("#table-view", Table)
        table_view.clear()
        try:
            table = TableFabric.fabric_without_rename(str(event.path))
            table_view.add_columns(*[i for i in range(0, len(table.keys()))])
            table_view.add_row(*table_view.create_header(table))
            name = [i for i in table.keys()][0]
            for i in range(0, len(table[name])):
                row = table_view.create_row(i, table)
                table_view.add_row(*row)
        except PermissionError as ex:
            Logger.write_error(ex)

    def action_open_path(self):
        tree = self.query_one("#file-tree-view", FileTree)
        directory = filedialog.askdirectory()
        tree.path = directory

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
