from unittest import TestCase

from valuer import SubEstimate
from valuer.app import AIHandler


class AiTest(TestCase):
    ai = AIHandler()

    def test_est(self):
        print([str(SubEstimate.create_empty())])

    def test_question(self):
        x = [SubEstimate(
            name="Валка берез",
            cost=100,
            cost_of_quantity=10,
            quantity=10,
            unit="дерево"
        ),
            SubEstimate(
                name="Валка дубов",
                cost=100,
                cost_of_quantity=10,
                quantity=10,
                unit="дерево"
            ),
            SubEstimate(
                name="Построить завод",
                cost=200000,
                cost_of_quantity=10,
                quantity=10,
                unit="шт"
            ),
        ]
        y = self.ai.parse(x)
        print(y)
