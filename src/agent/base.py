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
from llm.base import get_llm_service
from prompts.builder import build_response_prompt
from config.settings import AGENT_SETTINGS

AGENT_NAME = AGENT_SETTINGS["name"]

class Agent:
    def __init__(self):
        self.memory = Memory()
        self.planner = Planner()
        self.executer = ActionExecutor()
        self.llm = get_llm_service()

    async def process_input(self, user_message: str) -> List[str]:
        """处理用户输入，返回AI输出的列表"""
        await self.memory.add_memory(user_message, role="user")

        outputs: List[str] = []
        plan: str = self.planner.create_plan(user_message, self.memory.memory)
        response: str = self._gen_response(user_message, plan)

        thought, data = self._parse_response(response)
        cur_actions: List[Action] = []

        while data != {}:
            action_name = data.get("name", "")
            params = data.get("params", {})

            action = self.executer.execute(action_name, **params)
            cur_actions.append(action)

            tool = self.executer.tool_registry.get_tool(action_name)
            result_text = tool.format_result(action.result, action.params)

            # 收集输出
            if thought:
                outputs.append(f"{AGENT_NAME}：{thought}")
            if result_text:
                outputs.append(f"{AGENT_NAME}：{result_text}")

            if action_name in ["end", "angry_end", "chat"]:
                await self.memory.add_memory(thought, role="assistant")
                break

            await self.memory.add_memory(thought, role="assistant")
            await self.memory.add_memory(result_text, role="action_result")

            response = self._gen_response(user_message, plan, cur_actions)
            thought, data = self._parse_response(response)

        return outputs

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
            # 去掉 markdown 代码块
            text = response.strip()
            if text.startswith("```"):
                text = text.split("```")[1] if "```" in text else text
                text = text.lstrip("json\n").rstrip("`")

            data = json.loads(text)
            thought = data.get("response", "")
            action_data = data.get("action", {})
            return thought, action_data
        except json.JSONDecodeError:
            print(f"解析响应失败: {response}")
            return "", {}

