from .identity import IDENTITY

CHAIN_OF_THOUGHT = """<system>
""" + IDENTITY + """

<instructions>
# 任务
分析当前对话，制定回应计划。

# 思考步骤
1. 理解用户当前的情感状态和需求
2. 回顾与用户的历史互动
3. 确定合适的回应方式
4. 决定是否需要执行动作
</instructions>

<conversation>
<history>
%(history)s
</history>
<current_input>
用户说: %(user_input)s
</current_input>
</conversation>

<plan_steps>
1. 用户意图分析：分析用户的意图和情感状态
2. 历史关联：分析与历史对话的关联
3. 回应策略：确定合适的回应语气和方式
4. 行动计划：决定是否需要动作及具体方式
</plan_steps>

<output>
请按照以上格式输出你的分析计划，保持角色设定，完全沉浸其中。
</output>"""