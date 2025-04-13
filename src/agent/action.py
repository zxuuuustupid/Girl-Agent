
from typing import Any, Dict
from dataclasses import dataclass

_FUNCTION = Any

@dataclass
class Action:
    action_name: str
    params: Dict[str, Any]
    result: Any

class ActionExecutor:

    def __init__(self):
        self.available_actions = {}

    def register_action(self, name: str, action_fn: _FUNCTION):
        self.available_actions[name] = action_fn

    def execute(self, action_name, **params) -> Action:
        result = self.available_actions[action_name](**params)
        action = Action(action_name, params, result)
        return action