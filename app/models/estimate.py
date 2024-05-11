from dataclasses import dataclass


@dataclass
class Estimate:
    name: str
    workload: float
    cost: float

    @staticmethod
    def create_empty():
        return Estimate(
            name="",
            workload=0.0,
            cost=0.0
        )
