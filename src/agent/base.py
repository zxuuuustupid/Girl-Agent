from typing import Any, List, Tuple, Dict
import json
# import os
# import sys
#
# ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(ROOT_DIR)
from .plan import Planner
from .memory import Memory
from .action import Action, ActionExecutor
from llm.base import LLMService, DeepSeekService
from prompts.builder import build_response_prompt

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.planner = Planner()
        self.executer = ActionExecutor()
        self.llm = DeepSeekService()

    async def process_input(self, user_message: str) -> str:
        await self.memory.add_memory(user_message, role="user")
        """处理用户输入，返回AI回复"""
        # 生成plan用作后续迭代的cot
        plan: str = self.planner.create_plan(user_message,self.memory.memory)
        # 生成回复
        response: str = self._gen_response(user_message, plan)

        thought, data = self._parse_response(response)
        cur_actions: List[Action] = []

        # 不断迭代执行action
        while data != {}:
            action_name = data.get("name", "")
            params = data.get("params", {})

            action = self.executer.execute(action_name, **params)
            cur_actions.append(action)

            tool = self.executer.tool_registry.get_tool(action_name)
            if action_name in ["end","angry_end","chat"]:
                await self.memory.add_memory(thought, role="assistant")
                break

            await self.memory.add_memory(thought, role="assistant")
            result_text = tool.format_result(action.result, action.params)
            await self.memory.add_memory(result_text, role="action_result")

            response = self._gen_response(user_message, plan, cur_actions)
            thought, data = self._parse_response(response)

            return thought

    def _gen_response(self,
                     user_message: str,
                     plan: str,
                     actions: List[Action] = []) -> str:
        prompt = build_response_prompt(
            user_message=user_message,
            plan=plan,
            actions=actions,
            history=self.memory.memory
        )
        # print(prompt)
        # print()
        return self.llm.call(prompt)

    def _parse_response(self, response: str) -> Tuple[str, Dict[str, Any]]:
        try:
            data = json.loads(response)
            thought = data.get("response", "")
            action_data = data.get("action", {})
            return thought, action_data
        except json.JSONDecodeError:
            print(f"解析响应失败: {response}")
            return "", {}

