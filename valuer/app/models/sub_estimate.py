from dataclasses import dataclass


@dataclass
class SubEstimate:
    name: str
    unit: str
    quantity: float
    cost_of_quantity: float
    cost: float

    @staticmethod
    def create_empty():
        return SubEstimate(
            name="",
            unit="",
            quantity=0.0,
            cost_of_quantity=0.0,
            cost=0.0
        )

    @staticmethod
    def create_by_tuple(tuple_: tuple):
        return SubEstimate(
            name=tuple_[0],
            unit=tuple_[1],
            quantity=tuple_[2],
            cost_of_quantity=tuple_[3],
            cost=tuple_[4]
        )

    @staticmethod
    def create_by_dict(dict_: dict):
        return SubEstimate(
            name=dict_["name"],
            unit=dict_["unit"],
            quantity=dict_["quantity"],
            cost_of_quantity=dict_["cost_of_quantity"],
            cost=dict_["cost"]
        )

    def is_full_estimate(self):
        return str(self.cost_of_quantity) != "nan" and str(self.unit) != "nan" and \
               str(self.cost) != "nan"

    def __str__(self):
        return "{" + f"'name': {self.name}, 'cost': {self.cost}, 'unit': {self.unit}, 'quantity': {self.quantity}" + "}"
