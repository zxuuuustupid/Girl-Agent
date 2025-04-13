import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agent.plan import Planner
from src.agent.memory import MemoryItem

def test_create_plan():
    planner = Planner()
    history = [
        MemoryItem(
            user_input="你好啊",
            ai_response="你好呀，见到你真开心~",
            timestamp=datetime.now(),
            actions=[]
        ),
        MemoryItem(
            user_input="今天天气真好",
            ai_response="是啊，阳光明媚的，要不要一起出去玩呢？",
            timestamp=datetime.now(),
            actions=[]
        )
    ]

    user_message = "我今天心情不太好"
    plan = planner.create_plan(user_message, history)
    assert plan
    print(plan)

if __name__ == '__main__':
    test_create_plan()