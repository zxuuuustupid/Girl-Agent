from src.prompts.identity import IDENTITY

PLAN_FORMAT = """1. 用户意图分析：[分析用户的意图和情感状态]
2. 历史关联：[分析与历史对话的关联，如果有的话]
3. 行动计划：[详细描述打算如何回应，包括可能的行动]"""

CHAIN_OF_THOUGHT = f"""{IDENTITY}

# 对话信息
## 历史对话记录
{{history}}
## 当前对话
用户说: {{user_input}}

# 思考过程
1. 理解用户当前的情感状态和需求
2. 回顾我们之前的互动历史
3. 决定最合适的回应方式

# 执行计划
{{plan_format}}

请根据以上信息制定行动计划用作后续回应的参考。记住要保持你的人设。"""
