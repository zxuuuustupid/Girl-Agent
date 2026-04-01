# src/main.py

import sys
import os
import asyncio

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)
# print(ROOT_DIR)

# ANSI color codes
COLOR_PINK = "\033[95m"
COLOR_YELLOW = "\033[93m"
COLOR_GREEN = "\033[92m"
COLOR_RESET = "\033[0m"

def colored_output(text):
    """为输出添加颜色：名字粉色，文本黄色"""
    if "：" in text:
        name, content = text.split("：", 1)
        return f"{COLOR_PINK}{name}：{COLOR_RESET}{COLOR_YELLOW}{content}{COLOR_RESET}"
    return f"{COLOR_YELLOW}{text}{COLOR_RESET}"

from agent.base import Agent

async def run_chat():
    agent = Agent()
    print("你的女友已上线，开始聊天吧！")

    while True:
        try:
            user_input = input(f"\n{COLOR_GREEN}你{COLOR_RESET}: ").strip()

            if user_input.lower() in ['exit', 'quit', '退出']:
                print("\n再见啦！期待下次见面哦～")
                break

            if not user_input:
                continue

            outputs = await agent.process_input(user_message=user_input)
            for out in outputs:
                print(colored_output(out))

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
