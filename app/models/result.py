from dataclasses import dataclass
from app.models import Estimate


@dataclass
class Result:
    name: str
    estimates: [Estimate]
    global_workload: float
    global_cost: float

    @staticmethod
    def create_empty():
        return Result(
            name="",
            estimates=[],
            global_workload=0.0,
            global_cost=0.0
        )
