from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable
from app.view import *
from icecream import ic


class ValuerApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header(name="Valuer")
        yield Footer()
        yield Table()
        yield FileTree()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
