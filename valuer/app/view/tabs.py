from textual.app import ComposeResult
from textual.widgets import Input, TabPane
from textual.containers import *
from valuer.app import Config
from valuer.app.view.input_block import InputBlock


class Tabs:
    @staticmethod
    def compose() -> ComposeResult:
        yield Tabs.CCP("ССР", id="main")
        for i, config in enumerate(Config()["file"]["local-file"]):
            yield InputBlock(i + 1, config)
        yield Tabs.Plus("+")

    class CCP(TabPane):
        def compose(self) -> ComposeResult:
            config = Config()
            with Horizontal():
                with Container():
                    yield Input(id="name",
                                placeholder="name", value=config["file"]["name"])
                    yield Input(id="start-row",
                                placeholder="start row", value=config["file"]["start-row"])
                    yield Input(id="file",
                                placeholder="file path", value=config["entry-point"]["main-file"])
                with Container():
                    yield Input(id="cost",
                                placeholder="cost", value=config["file"]["cost"])
                    yield Input(id="end-row",
                                placeholder="end row", value=config["file"]["end-row"])
                    yield Input(id="output",
                                placeholder="output file", value=config["entry-point"]["output"])

    class Plus(TabPane):
        def compose(self) -> ComposeResult:
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
