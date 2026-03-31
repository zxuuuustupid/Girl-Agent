from openai import OpenAI
from anthropic import Anthropic
from abc import ABC, abstractmethod
import httpx
from config.settings import DEEPSEEK_SETTINGS, ZHIPU_SETTINGS, MINIMAX_SETTINGS, LLM_PROVIDER

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

class ZhipuService(LLMService):

    def __init__(self):
        self._llm_client = OpenAI(
            api_key=ZHIPU_SETTINGS["api_key"],
            base_url=ZHIPU_SETTINGS["api_base"],
        )

    def call(self, prompt: str) -> str:
        response = self._llm_client.chat.completions.create(
            model=ZHIPU_SETTINGS["model"],
            messages=[{
                "role": "user",
                "content": prompt
            }])

        return response.choices[0].message.content.strip()

class MiniMaxService(LLMService):

    def __init__(self):
        self._api_key = MINIMAX_SETTINGS["api_key"]
        self._model = MINIMAX_SETTINGS["model"]
        self._client = httpx.Client(timeout=60.0)
        self._url = "https://api.minimax.chat/v1/text/chatcompletion_v2"

    def call(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        response = self._client.post(self._url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

def get_llm_service() -> LLMService:
    """根据配置返回对应的LLM服务实例"""
    if LLM_PROVIDER == "zhipu":
        return ZhipuService()
    elif LLM_PROVIDER == "minimax":
        return MiniMaxService()
    else:
        return DeepSeekService()