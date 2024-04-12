from dataclasses import dataclass


@dataclass
class Estimate:
    name: str
    unit: str
    workload: str
    cost: int
