from unittest import TestCase
from valuer.app import AIHandler


class AiTest(TestCase):
    ai = AIHandler()

    def test_question(self):
        msg = self.ai.send_message("Whats your name?")
        print(msg)
