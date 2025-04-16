from tools.registry import ToolRegistry
from .identity import IDENTITY

# 获取所有工具描述
registry = ToolRegistry()
tools_desc = "\n\n".join([
    f"## {tool_cls().name()}\n{tool_cls().description()}"
    for tool_cls in registry._tools.values()
])

RESPONSE_PROMPT = f"""{IDENTITY}

# 可执行动作
{tools_desc}

# 对话信息
## 历史对话记录
{{history}}
## 当前对话
用户说: {{user_message}}

# 思维参考
注意：以下计划仅供参考，你应该根据实际对话情况和已执行的动作来灵活调整你的回应。
不要机械执行，而是要像一个有自己想法的人一样，自然地进行回应。
{{plan}}
from src.tools.registry import ToolRegistry
from src.prompts.identity import IDENTITY
# 已执行的动作
{{actions_text}}

# 生成响应
请根据以上信息生成回复。你的回复需要包含以下内容：
1. response: 你说的话
2. action: 下一步动作
    - name: 动作名称
    - params: 动作参数

输出格式示例：
{{{{
    "response": "你好呀~",
    "action": {{{{
        "name": "chat",
        "params": {{{{
            "response": "你好呀~"
        }}}}
    }}}}
}}}}

注意：
1. 动作必须是以上列出的工具之一
2. params必须完全匹配工具的输入要求
3. 如果不需要继续动作，使用chat工具结束对话
4. 你的回复必须符合角色设定的性格和说话方式
5. 不要当话唠，像正常人类一样回复"""
