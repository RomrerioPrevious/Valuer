from textual.app import ComposeResult
from textual.containers import Horizontal, Container
from textual.widget import Widget
from textual.widgets import TabPane, Input


class InputBlock(TabPane):
    def __init__(self, num: int, settings: dict, *children: Widget):
        super().__init__(f"Variation: {num}")
        self.num = num
        self.settings = settings

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Container():
                yield Input(id=f"name-var{self.num}",
                            placeholder="name", value=str(self.settings["name"]))
                yield Input(id=f"quantity-var{self.num}",
                            placeholder="quantity", value=str(self.settings["quantity"]))
                yield Input(id=f"start-row-var{self.num}",
                            placeholder="start row", value=str(self.settings["start-row"]))
            with Container():
                yield Input(id=f"unit-var{self.num}",
                            placeholder="unit", value=str(self.settings["unit"]))
                yield Input(id=f"cost-of-quantity-var{self.num}",
                            placeholder="cost of quantity", value=str(self.settings["cost-of-quantity"]))
                yield Input(id=f"cost-var{self.num}",
                            placeholder="cost", value=str(self.settings["cost"]))
