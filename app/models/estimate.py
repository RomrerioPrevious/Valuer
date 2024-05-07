from dataclasses import dataclass


@dataclass
class Estimate:
    name: str
    unit: str
    workload: str
    cost: int

    @staticmethod
    def create_empty():
        return Estimate(
            name="",
            unit="",
            workload="",
            cost=0
        )
