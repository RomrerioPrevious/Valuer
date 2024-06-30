from app.config import Config
from transformers import pipeline
from app.models import Estimate
from app.models.sub_estimate import SubEstimate


class AIHandler:
    def __init__(self):
        self.config = Config()
        self.ai_config = self.config["ai"]
        self.clf = pipeline("question-answering")
        with open("/resources/data/ai-contex.txt") as file:
            self.contex = file.read()

    def check(self, estimate: Estimate) -> Estimate:
        titels = [(i.name, i.unit, i.quantity, i.cost_of_quantity) for i in estimate.sub_estimates]
        question = f"Объедени эти заголовки до 5 новых заголовков с разделением ';'. Вот заголовки: {titels}."
        result = self.send_message(question).split(";")
        estimate.sub_estimates = []
        for i in result:
            estimate.sub_estimates = SubEstimate.create_by_tuple(i)
        return estimate

    def send_message(self, question: str) -> str:
        return self.clf(question, self.contex)
