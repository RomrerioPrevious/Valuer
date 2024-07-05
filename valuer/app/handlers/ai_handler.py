import ast

from icecream import ic

from valuer.app.config import Config, Logger
from valuer.app.models import SubEstimate
import requests


class AIHandler:
    def __init__(self):
        self.config = Config()
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.header = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.config['ai']['api']}"
        }

    def parse(self, sub_estimates: [SubEstimate]) -> [SubEstimate]:
        massages = self.generate_messages(sub_estimates)
        result = self.send_message(massages)
        for i in range(0, len(result)):
            try:
                result[i] = SubEstimate.create_by_dict(result[i])
            except BaseException as ex:
                Logger.write_error(ex)
        return result

    def send_message(self, messages: [str]) -> [dict]:
        result = []
        for message in messages:
            try:
                prompt = self.generate_prompt(message)
                responce = requests.post(self.url,
                                         headers=self.header,
                                         json=prompt)
                temp = ast.literal_eval(responce.text)["result"]["alternatives"][0]["message"]["text"]
                temp = ast.literal_eval(self.formatting_temp(temp))
                result += temp
            except BaseException as ex:
                Logger.write_error(ex)
        return result

    def generate_prompt(self, message: str) -> dict:
        return {
            "modelUri": f"gpt://{self.config['ai']['id']}/yandexgpt",
            "completionOptions": {
                "stream": False,
            },
            "messages": [
                {"role": "user", "text": message}
            ]
        }

    def generate_messages(self, sub_estimates: [SubEstimate]) -> [str]:
        path = f"{Config.find_global_path()}\\resources\\data\\ai-contex.txt"
        with open(path, "r", encoding="UTF-8") as file:
            text = file.read()
        result = []
        estimates_list = ""
        for i in sub_estimates:
            if len(estimates_list) + len(str(i)) >= 9400:
                result.append(f"""Есть список словарей: {f"[{estimates_list}]"}. {text}""")
                estimates_list = ""
            estimates_list += f"{str(i)}, "
        if estimates_list != "":
            result.append(f"""Есть список словарей: {f"[{estimates_list}]"}. {text}""")
        return result

    @staticmethod
    def formatting_temp(temp: str) -> str:
        if temp[0:4] == "json":
            return temp[3:]
        elif temp[0:7] == "```json":
            return temp[6:len(temp) - 6]
        return temp
