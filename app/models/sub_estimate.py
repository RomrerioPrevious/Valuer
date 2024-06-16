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

    @staticmethod
    def create_by_tuple(tuple_: tuple):
        return SubEstimate(
            name=tuple_[0],
            unit=tuple_[1],
            quantity=tuple_[2],
            cost_of_quantity=tuple_[3]
        )
