from time import sleep

from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Header, Footer, Input, DirectoryTree, TabbedContent
from tkinter import filedialog
from valuer.app import *
from icecream import ic
from configparser import ConfigParser


class ValuerApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Theme"),
                ("ctrl+p", "open_path", "Open path"),
                ("ctrl+s", "save", "Save"),
                ("ctrl+r", "start", "Start")]
    CSS_PATH = "resources/style/index.tcss"

    def compose(self) -> ComposeResult:
        yield Header(name="Valuer")
        with Container():
            yield FileTree(id="file-tree-view", path="C:\\")
            with Vertical(id="work-zone"):
                yield Table(id="table-view", show_header=False)
                with TabbedContent(id="tabs"):
                    yield from Tabs().compose()
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

    def action_start(self):
        handler = FileHandler()
        path = str(self.query_one("#file-tree-view", FileTree).path) + "\\"
        Config()["entry-point"]["input"] = path
        self.update_config()
        handler.parse()

    def action_save(self):
        tab = self.query_one("#tabs", TabbedContent).active_pane
        type_of_tab = type(tab)
        if type_of_tab is InputBlock:
            id = int(tab.id[4:])
            self.get_from_input_block(id)
        elif type_of_tab is Tabs.CCP:
            self.get_from_main_block()
        else:
            id = int(tab.id[4:])
            self.get_from_add_block(id)
            self.create_tabbed_content()
        self.update_config()

    def create_tabbed_content(self):
        tabs = self.query_one("#tabs", TabbedContent)
        tabs.clear_panes()
        tabs.add_pane(Tabs.CCP("СРР"))
        for i, config in enumerate(Config()["file"]["local-file"]):
            tabs.add_pane(InputBlock(i + 1, config))
        tabs.add_pane(Tabs.Plus("+"))

    @staticmethod
    def update_config():
        configparser = ConfigParser()
        config = Config()
        configparser.read_dict(config)
        with open(Config.find_config_path(), "w", encoding="UTF-8") as file:
            configparser.write(file)

    def get_from_main_block(self):
        config = Config()
        values = [
            "name",
            "start-row",
            "end-row",
            "cost"
        ]
        for i in values:
            value = self.query_one(f"#{i}", Input).value
            try:
                value = int(value)
                config["file"][i] = value
            except ValueError:
                ...
        config["entry-point"]["main-file"] = self.query_one("#file", Input).value
        config["entry-point"]["output"] = self.query_one("#output", Input).value

    def get_from_add_block(self, id: int):
        config = Config()
        values = [
            "name",
            "unit",
            "start-row",
            "quantity",
            "cost-of-quantity",
            "cost"
        ]
        config["file"]["local-file"].append({})
        for i in values:
            value = self.query_one(f"#{i}-var", Input).value
            try:
                value = int(value)
                config["file"]["local-file"][id - 2][i] = value
            except ValueError:
                ...

    def get_from_input_block(self, id: int):
        config = Config()
        values = [
            "name",
            "unit",
            "start-row",
            "quantity",
            "cost-of-quantity",
            "cost"
        ]
        for i in values:
            value = self.query_one(f"#{i}-var{id - 1}", Input).value
            try:
                value = int(value)
                config["file"]["local-file"][id - 2][i] = value
            except ValueError:
                ...

    def action_open_path(self):
        tree = self.query_one("#file-tree-view", FileTree)
        directory = filedialog.askdirectory()
        tree.path = directory

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
