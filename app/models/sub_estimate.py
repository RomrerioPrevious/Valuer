from dataclasses import dataclass


@dataclass
class SubEstimate:
    name: str
    unit: str
    quantity: float
    cost_of_quantity: float

    @staticmethod
    def create_empty():
        return SubEstimate(
            name="",
            unit="",
            quantity=0.0,
            cost_of_quantity=0.0
        )
