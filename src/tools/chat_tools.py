from typing import Any

from config.settings import AGENT_SETTINGS

from .interaction_context import request_confirmation, request_number
from .tool_interface import Tool


class ChatTool(Tool):
    def name(self) -> str:
        return "chat"

    def description(self) -> str:
        return (
            "Normal chat reply.\n"
            "Parameters:\n"
            "- response: str, the assistant message to show.\n"
            "Returns:\n"
            "- None"
        )

    def run(self, response: str, **kwargs) -> Any:
        return f"{AGENT_SETTINGS['name']}: {response}"

    def format_result(self, result: Any, params: dict) -> str:
        return ""


class AskGiftTool(Tool):
    def name(self) -> str:
        return "ask_gift"

    def description(self) -> str:
        return (
            "Ask the user for a gift.\n"
            "Parameters:\n"
            "- response: str, text shown before asking.\n"
            "- gift_name: str, the requested gift.\n"
            "Returns:\n"
            "- gift_given: bool"
        )

    def run(self, response: str, gift_name: str, **kwargs) -> Any:
        display_text = f"{AGENT_SETTINGS['name']}: {response}\nRequested gift: {gift_name}"
        accepted = request_confirmation(
            title="Gift Request",
            message=f"{response}\nGift: {gift_name}",
            confirm_label="Accept",
            cancel_label="Refuse",
        )
        return accepted, display_text

    def format_result(self, result: Any, params: dict) -> str:
        accepted, display_text = result
        if accepted:
            return f"{display_text}\nYou agreed to give {params['gift_name']}."
        return f"{display_text}\nYou refused to give {params['gift_name']}."


class GiveGiftTool(Tool):
    def name(self) -> str:
        return "give_gift"

    def description(self) -> str:
        return (
            "Give the user a gift.\n"
            "Parameters:\n"
            "- response: str, text shown before the gift.\n"
            "- gift_name: str, the gift that is given.\n"
            "Returns:\n"
            "- None"
        )

    def run(self, response: str, gift_name: str, **kwargs) -> Any:
        return f"{AGENT_SETTINGS['name']}: {response}\nGift given: {gift_name}"

    def format_result(self, result: Any, params: dict) -> str:
        return ""


class AskCoinsTool(Tool):
    def name(self) -> str:
        return "ask_coins"

    def description(self) -> str:
        return (
            "Ask the user for coins.\n"
            "Parameters:\n"
            "- response: str, text shown before asking.\n"
            "- amount: int, suggested amount.\n"
            "Returns:\n"
            "- coins: int"
        )

    def run(self, response: str, amount: int, **kwargs) -> Any:
        display_text = f"{AGENT_SETTINGS['name']}: {response}\nRequested coins: {amount}"
        coins = request_number(
            title="Coin Request",
            message=f"{response}\nRequested coins: {amount}",
            default=amount,
            minimum=0,
        )
        return coins, display_text

    def format_result(self, result: Any, params: dict) -> str:
        coins, display_text = result
        return f"{display_text}\nYou offered {coins} coins."


class IntimateActionTool(Tool):
    def name(self) -> str:
        return "intimate_action"

    def description(self) -> str:
        return (
            "Perform an intimate action in text.\n"
            "Parameters:\n"
            "- response: str, assistant narration.\n"
            "- action: str, the action description.\n"
            "Returns:\n"
            "- None"
        )

    def run(self, response: str, action: str, **kwargs) -> Any:
        return f"{AGENT_SETTINGS['name']}: {response}\n[Action]: {action}"

    def format_result(self, result: Any, params: dict) -> str:
        return ""


class AngryEndTool(Tool):
    def name(self) -> str:
        return "angry_end"

    def description(self) -> str:
        return (
            "End the conversation in an angry way.\n"
            "Parameters:\n"
            "- response: str, final angry response.\n"
            "Returns:\n"
            "- None"
        )

    def run(self, response: str, **kwargs) -> Any:
        return f"{AGENT_SETTINGS['name']}: {response}\n[Conversation closed]"

    def format_result(self, result: Any, params: dict) -> str:
        return ""
