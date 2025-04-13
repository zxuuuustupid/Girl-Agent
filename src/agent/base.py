from typing import Any, List, Tuple, Dict
from src.agent.plan import Planner
from src.agent.memory import Memory
from src.agent.action import Action, ActionExecutor

class Agent:

    def __init__(self):
        self.memory = Memory()
        self.planner = Planner()
        self.executer = ActionExecutor()

    def process_input(self, user_message: str) -> str:
        """处理用户输入，返回AI回复"""
        # 生成plan用作后续迭代的cot​
        plan: str = self.planner.create_plan(user_message)
        # 生成回复​
        response: str = self._gen_response(user_message, plan)

        thought, data = self._parse_response(response)
        actions: List[Action] = []
        # 不断迭代执行action​
        while data != {} and data.get("action_name", "end") != "end":
            action_name = data.get("action_name", "")
            params = data.get("params", {})
            action = self.executer.execute(action_name, **params)
            actions.append(action)
            response = self._gen_response(user_message, plan, actions)
            thought, data = self._parse_response(response)
        self.memory.add_memory(user_message, thought, actions)
        return thought

    def _gen_response(self,
                      user_message: str,
                      plan: str,
                      actions: List[Action] = []) -> str:
        pass

    def _parse_response(self, response: str) -> Tuple[str, Dict[str, Any]]:
        pass