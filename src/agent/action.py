from dataclasses import dataclass
from typing import Any, Dict

from tools.registry import ToolRegistry

_FUNCTION = Any


@dataclass
class Action:
    action_name: str
    params: Dict[str, Any]
    result: Any


class ActionExecutor:
    def __init__(self):
        self.tool_registry = ToolRegistry()

    def execute(self, action_name: str, **kwargs) -> Action:
        resolved_name = self.tool_registry.resolve_tool_name(action_name)
        payload = dict(kwargs)

        # Let the model invent soft actions like kiss/cuddle/hug without failing.
        if resolved_name == "intimate_action":
            payload.setdefault("action", action_name)
            payload.setdefault("response", kwargs.get("response", ""))
        elif resolved_name == "chat":
            payload.setdefault("response", kwargs.get("response", ""))

        try:
            tool = self.tool_registry.get_tool(action_name)
            result = tool.run(**payload)
            return Action(
                action_name=resolved_name,
                params=payload,
                result=result,
            )
        except Exception as e:
            print(f"执行动作 {action_name} 时出错: {str(e)}")
            return Action(
                action_name=resolved_name,
                params=payload,
                result={"status": "error", "message": str(e)},
            )
