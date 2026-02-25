from typing import List
from .memory import MemoryItem
from llm.base import get_llm_service
from prompts.builder import build_plan_prompt

class Planner:

    def __init__(self):
        self.llm = get_llm_service()

    def create_plan(self, user_message: str, history: List[MemoryItem]) -> str:
        prompt = build_plan_prompt(user_message, history)
        # print(f'plan prompt: \n{prompt}')
        return self.llm.call(prompt)