from openai import OpenAI
from abc import ABC, abstractmethod
from config.settings import DEEPSEEK_SETTINGS, ZHIPU_SETTINGS, ZHIZENG_SETTINGS, LLM_PROVIDER

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

class ZhizengService(LLMService):

    def __init__(self):
        self._llm_client = OpenAI(
            api_key=ZHIZENG_SETTINGS["api_key"],
            base_url=ZHIZENG_SETTINGS["api_base"],
        )

    def call(self, prompt: str) -> str:
        response = self._llm_client.chat.completions.create(
            model=ZHIZENG_SETTINGS["model"],
            messages=[{
                "role": "system",
                "content": prompt
            }])

        return response.choices[0].message.content.strip()

class MiniMaxService(LLMService):

    def __init__(self):
        import anthropic

        from config.settings import MINIMAX_API_KEY, MINIMAX_API_BASE, MINIMAX_MODEL
        self._client = anthropic.Anthropic(
            api_key=MINIMAX_API_KEY,
            base_url=MINIMAX_API_BASE,
        )
        self._model = MINIMAX_MODEL

    def call(self, prompt: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            system=prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        text_blocks = [block.text for block in response.content if block.type == "text"] if response.content else []
        return "\n".join(text_blocks) if text_blocks else ""

def get_llm_service() -> LLMService:
    """根据配置返回对应的LLM服务实例"""
    if LLM_PROVIDER == "zhipu":
        return ZhipuService()
    elif LLM_PROVIDER == "minimax":
        return MiniMaxService()
    elif LLM_PROVIDER == "zhizeng":
        return ZhizengService()
    else:
        return DeepSeekService()
