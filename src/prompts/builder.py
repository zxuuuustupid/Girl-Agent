from typing import List
from src.agent.memory import MemoryItem
from src.config.settings import AGENT_SETTINGS
from src.prompts.chain_of_thought import CHAIN_OF_THOUGHT, PLAN_FORMAT

def build_plan_prompt(user_input: str, history: List[MemoryItem]) -> str:
    history_lines = []
    for item in history:
        history_lines.extend([
            f"用户: {item.user_input}",
            f"{AGENT_SETTINGS['name']}: {item.ai_response}"
        ])
    history_text = "\n".join(history_lines) if history_lines else "无历史对话记录"

    return CHAIN_OF_THOUGHT.format(
        history=history_text,
        user_input=user_input,
        plan_format=PLAN_FORMAT
    )