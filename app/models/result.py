from dataclasses import dataclass
from app.models import Estimate


@dataclass
class Result:
    name: str
    estimates: [Estimate]
    global_cost: float

    @staticmethod
    def create_empty():
        return Result(
            name="",
            estimates=[],
            global_cost=0.0
        )

    @staticmethod
    def create_with_name(name: str):
        return Result(
            name=name,
            estimates=[],
            global_cost=0.0
        )
