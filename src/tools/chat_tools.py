from typing import Any
from .tool_interface import Tool
from config.settings import AGENT_SETTINGS

class ChatTool(Tool):
    def name(self) -> str:
        return "chat"

    def description(self) -> str:
        return """继续和用户聊天
输入:
- response: str, 你的回复内容
输出:
- None """

    def run(self, response: str, **kwargs) -> Any:
        print(f"\n{AGENT_SETTINGS['name']}: {response}")
        return None

    def format_result(self, result: Any, params: dict) -> str:
        return ""

class AskGiftTool(Tool):
    def name(self) -> str:
        return "ask_gift"

    def description(self) -> str:
        return """向用户索要礼物
输入:
- response: str, 你的请求礼物的话
- gift_name: str, 想要的礼物的具体名称
输出:
- gift_given: bool，用户是否同意送礼物"""

    def run(self, response: str, gift_name: str, **kwargs) -> Any:
        print(f"\n{AGENT_SETTINGS['name']}: {response}")
        print(f"\n想要的礼物是: {gift_name}")
        user_input = input("\n是否愿意送出这个礼物？(y/n): ").lower()
        return user_input.startswith('y')

    def format_result(self, result: Any, params: dict) -> str:
        if result:
            return f"用户同意了送给你{params['gift_name']}！"
        return "用户拒绝了送出礼物的请求"

class GiveGiftTool(Tool):
    def name(self) -> str:
        return "give_gift"

    def description(self) -> str:
        return """送给用户礼物
输入:
- response: str, 你的送礼物的话语
- gift_name: str, 要送的礼物的具体名称
输出:
- None """

    def run(self, response: str, gift_name: str, **kwargs) -> Any:
        print(f"\n{AGENT_SETTINGS['name']}: {response}")
        print(f"\n送给你的礼物是: {gift_name}")
        return None

    def format_result(self, result: Any, params: dict) -> str:
        return ""

class AskCoinsTool(Tool):
    def name(self) -> str:
        return "ask_coins"

    def description(self) -> str:
        return """向用户索要金币
输入:
- response: str, 你的请求金币的话语
- amount: int, 想要的金币数量
输出:
- coins: int, 用户给的金币数量"""

    def run(self, response: str, amount: int, **kwargs) -> Any:
        print(f"\n{AGENT_SETTINGS['name']}: {response}")
        print(f"\n想要爆你 {amount} 个金币")
        user_input = input("\n请输入要给的金币数量: ")
        return int(user_input)

    def format_result(self, result: Any, params: dict) -> str:
        return f"用户给了你{result}个金币"

class IntimateActionTool(Tool):
    def name(self) -> str:
        return "intimate_action"

    def description(self) -> str:
        return """向用户执行亲昵动作
输入:
- response: str, 你的话语
- action: str, 要执行的亲昵动作
输出:
- None """

    def run(self, response: str, action: str, **kwargs) -> Any:
        print(f"\n{AGENT_SETTINGS['name']}: {response}")
        print(f"\n[执行动作]: {action}")
        return None

    def format_result(self, result: Any, params: dict) -> str:
        return ""

class AngryEndTool(Tool):
    def name(self) -> str:
        return "angry_end"

    def description(self) -> str:
        return """气愤地结束对话
输入:
- response: str, 你生气的话语
输出:
- None """

    def run(self, response: str, **kwargs) -> Any:
        print(f"\n{AGENT_SETTINGS['name']}: {response}")
        print("\n[对话结束]")
        return None

    def format_result(self, result: Any, params: dict) -> str:
        return  ""
