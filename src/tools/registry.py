from typing import Dict, Type

from .chat_tools import (
    AngryEndTool,
    AskCoinsTool,
    AskGiftTool,
    ChatTool,
    GiveGiftTool,
    IntimateActionTool,
)
from .tool_interface import Tool


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Type[Tool]] = {}
        self._aliases: Dict[str, str] = {}
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        default_tools = [
            ChatTool,
            AskGiftTool,
            GiveGiftTool,
            AskCoinsTool,
            IntimateActionTool,
            AngryEndTool,
        ]

        for tool_cls in default_tools:
            tool = tool_cls()
            self._tools[tool.name()] = tool_cls

        self._aliases.update(
            {
                "chat": "chat",
                "talk": "chat",
                "reply": "chat",
                "message": "chat",
                "speak": "chat",
                "聊天": "chat",
                "对话": "chat",
                "回复": "chat",
                "ask_gift": "ask_gift",
                "gift_request": "ask_gift",
                "request_gift": "ask_gift",
                "要礼物": "ask_gift",
                "索要礼物": "ask_gift",
                "give_gift": "give_gift",
                "send_gift": "give_gift",
                "present": "give_gift",
                "送礼物": "give_gift",
                "ask_coins": "ask_coins",
                "request_coins": "ask_coins",
                "coins": "ask_coins",
                "金币": "ask_coins",
                "要金币": "ask_coins",
                "intimate_action": "intimate_action",
                "intimate": "intimate_action",
                "affection": "intimate_action",
                "romance": "intimate_action",
                "romantic": "intimate_action",
                "flirt": "intimate_action",
                "kiss": "intimate_action",
                "hug": "intimate_action",
                "cuddle": "intimate_action",
                "caress": "intimate_action",
                "snuggle": "intimate_action",
                "touch": "intimate_action",
                "hold": "intimate_action",
                "pat": "intimate_action",
                "亲密": "intimate_action",
                "亲昵": "intimate_action",
                "亲亲": "intimate_action",
                "拥抱": "intimate_action",
                "贴贴": "intimate_action",
                "暧昧": "intimate_action",
                "调情": "intimate_action",
                "angry_end": "angry_end",
                "end": "angry_end",
                "结束": "angry_end",
            }
        )

    def resolve_tool_name(self, name: str) -> str:
        raw = (name or "").strip()
        if not raw:
            return "chat"

        if raw in self._tools:
            return raw
        if raw in self._aliases:
            return self._aliases[raw]

        lowered = raw.lower().replace("-", "_").replace(" ", "_")
        if lowered in self._tools:
            return lowered
        if lowered in self._aliases:
            return self._aliases[lowered]

        intimate_keywords = (
            "kiss",
            "cuddle",
            "hug",
            "snuggle",
            "caress",
            "flirt",
            "romance",
            "intimate",
            "affection",
            "touch",
            "hold",
            "love",
            "亲",
            "抱",
            "贴",
            "摸",
            "暧昧",
            "亲密",
        )
        gift_keywords = ("gift", "present", "礼物")
        coin_keywords = ("coin", "coins", "金币")

        if any(keyword in lowered for keyword in intimate_keywords) or any(keyword in raw for keyword in intimate_keywords):
            return "intimate_action"
        if any(keyword in lowered for keyword in gift_keywords) or any(keyword in raw for keyword in gift_keywords):
            return "ask_gift"
        if any(keyword in lowered for keyword in coin_keywords) or any(keyword in raw for keyword in coin_keywords):
            return "ask_coins"

        return "chat"

    def get_tool(self, name: str) -> Tool:
        normalized = self.resolve_tool_name(name)
        return self._tools[normalized]()
