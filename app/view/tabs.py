from icecream import ic
from textual.app import ComposeResult
from textual.widgets import Input, TabbedContent, TabPane, Static
from textual.containers import *
from app import Config
from app.view.input_block import InputBlock


class Tabs:
    @staticmethod
    def compose() -> ComposeResult:
        with TabPane("ССР", id="main"):
            with Horizontal():
                with Container():
                    yield Input(id="name", placeholder="name")
                    yield Input(id="start-row", placeholder="start row")
                    yield Input(id="file", placeholder="file path")
                with Container():
                    yield Input(id="cost", placeholder="cost")
                    yield Input(id="end-row", placeholder="end row")
                    yield Input(id="output", placeholder="output file")
        for i, config in enumerate(Config()["file"]["local-file"]):
            yield InputBlock(i + 1, config)
        with TabPane("+"):
            with Horizontal():
                with Container():
                    yield Input(id=f"name-var",
                                placeholder="name")
                    yield Input(id=f"quantity-var",
                                placeholder="quantity")
                    yield Input(id=f"start-row-var",
                                placeholder="start row")
                with Container():
                    yield Input(id=f"unit-var",
                                placeholder="unit")
                    yield Input(id=f"cost-of-quantity-var",
                                placeholder="cost of quantity")
                    yield Input(id=f"cost-var",
                                placeholder="cost")
