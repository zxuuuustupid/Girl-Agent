from openai import OpenAI
from abc import ABC, abstractmethod
from config.settings import DEEPSEEK_SETTINGS

class LLMService(ABC):

    @abstractmethod
    def call(self, prompt: str) -> str:
        pass

class DeepSeekService(LLMService):

    def __init__(self):
        self._llm_client = OpenAI(
            api_key=DEEPSEEK_SETTINGS["api_key"],
            base_url=DEEPSEEK_SETTINGS["api_base"],
        )

    def call(self, prompt: str) -> str:
        response = self._llm_client.chat.completions.create(
            model=DEEPSEEK_SETTINGS["model"],
            messages=[{
                "role": "system",
                "content": prompt
            }])

        return response.choices[0].message.content.strip()