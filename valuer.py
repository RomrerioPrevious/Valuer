from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Header, Footer, Static, DirectoryTree
from app.view import *
from icecream import ic


class ValuerApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode"),
                ("ctrl+p", "open_path", "Open path")]
    CSS_PATH = "resources/style/index.tcss"

    def compose(self) -> ComposeResult:
        yield Header(name="Valuer")
        with Container():
            yield FileTree(id="file-tree-view")
            with VerticalScroll(id="table-view"):
                yield Static(id="table", expand=True)
        yield Footer()

    def on_directory_tree_file_selected(
            self, event: DirectoryTree.FileSelected) -> None:
        event.stop()
        table_view = self.query_one("#table", Static)
        try:
            ...
        except:
            ...
        else:
            table_view.update()
            self.query_one("#table-view").scroll_home(animate=False)


    def action_open_path(self):
        ...

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
