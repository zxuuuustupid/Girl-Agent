# src/main.py

import sys
import os
import asyncio

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)
# print(ROOT_DIR)

from agent.base import Agent

async def run_chat():
    agent = Agent()
    print("你的女友已上线，开始聊天吧！")

    while True:
        try:
            user_input = input("\n你: ").strip()

            if user_input.lower() in ['exit', 'quit', '退出']:
                print("\n再见啦！期待下次见面哦～")
                break

            if not user_input:
                continue

            response = await agent.process_input(user_message=user_input)

        except KeyboardInterrupt:
            print("\n\n再见啦！期待下次见面哦～")
            break

def main():
    try:
        asyncio.run(run_chat())
    except KeyboardInterrupt:
        print("\n\n再见啦！期待下次见面哦～")
    sys.exit(0)

# 可选：保留这句用于直接运行 src/main.py 测试
if __name__ == "__main__":
    main()
