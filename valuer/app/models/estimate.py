from dataclasses import dataclass
from .sub_estimate import SubEstimate


@dataclass
class Estimate:
    name: str
    cost: float
    sub_estimates: [SubEstimate]

    @staticmethod
    def create_empty():
        return Estimate(
            name="",
            cost="",
            sub_estimates=[]
        )
