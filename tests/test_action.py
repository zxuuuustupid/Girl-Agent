import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.action import ActionExecutor

def test_action():
    executor = ActionExecutor()
    executor.execute(
        "chat",
        response="你好呀~"
    )
    executor.execute(
        "ask_gift",
        response="我想要一个布偶~",
        gift_name="布偶"
    )
    executor.execute(
        "give_gift",
        response="这是我给你的礼物~",
        gift_name="巧克力"
    )
    executor.execute(
        "ask_coins",
        response="我想要一些金币~",
        amount=100
    )
    executor.execute(
        "intimate_action",
        response="让我抱抱你~",
        action="轻轻抱住用户"
    )
    executor.execute(
        "angry_end",
        response="哼！不理你了！"
    )


if __name__ == '__main__':
    test_action()