from typing import List
from src.agent.memory import MemoryItem
from src.llm.base import DeepSeekService
from src.prompts.builder import build_plan_prompt

class Planner:

    def __init__(self):
        self.llm = DeepSeekService()

    def create_plan(self, user_message: str, history: List[MemoryItem]) -> str:
        prompt = build_plan_prompt(user_message, history)
        # print(f'plan prompt: \n{prompt}')
        return self.llm.call(prompt)