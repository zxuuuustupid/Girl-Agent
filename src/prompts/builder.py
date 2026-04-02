import json
from typing import List
from agent.action import Action
from agent.memory import MemoryItem
from .response import RESPONSE_PROMPT
from .chain_of_thought import CHAIN_OF_THOUGHT
from config.settings import AGENT_SETTINGS

# 根据性格决定对用户的称呼
_PERSONALITY_CALL = {
    "slaver": "主人",
    "slapper": "大人",
}
USER_CALL = _PERSONALITY_CALL.get(AGENT_SETTINGS["personality"], "男朋友")

def build_plan_prompt(user_input: str, history: List[MemoryItem]) -> str:
    history_lines = []
    for item in history:
        if item.role == "user":
            history_lines.append("<user>%s: %s</user>" % (USER_CALL, item.message))
        elif item.role == "assistant":
            history_lines.append("<assistant>你: %s</assistant>" % item.message)
        elif item.role == "action_result":
            history_lines.append("<action_result>%s</action_result>" % item.message)

    history_text = "\n".join(history_lines) if history_lines else "无历史对话记录"

    return CHAIN_OF_THOUGHT % {
        "user_input": user_input,
        "history": history_text
    }

def build_response_prompt(
    user_message: str,
    plan: str,
    actions: List[Action],
    history: List[MemoryItem]
) -> str:
    # 处理plan内容，移除所有一级标题（以单个#开头的行）
    plan_lines = []
    for line in plan.strip().split('\n'):
        if not line.strip().startswith('# ') or line.strip().startswith('## '):
            plan_lines.append(line)
    plan = '\n'.join(plan_lines).strip()

    # 构建对话历史
    history_lines = []
    for item in history:
        if item.role == "user":
            history_lines.append("<user>%s: %s</user>" % (USER_CALL, item.message))
        elif item.role == "assistant":
            history_lines.append("<assistant>你: %s</assistant>" % item.message)
        elif item.role == "action_result":
            history_lines.append("<action_result>%s</action_result>" % item.message)

    history_text = "\n".join(history_lines) if history_lines else "无历史对话记录"

    # 构建动作历史
    actions_text = "无已执行的动作"
    if actions:
        from tools.registry import ToolRegistry
        registry = ToolRegistry()
        action_lines = []
        for action in actions:
            # 获取对应的工具
            tool = registry.get_tool(action.action_name)
            if tool:
                # 格式化参数和结果
                params = tool.format_params(action.params)
                result_text = tool.format_result(action.result, action.params)

                # 构建动作描述
                action_desc = "- %s" % action.action_name
                if params:
                    action_desc += ": %s" % json.dumps(params, ensure_ascii=False)
                if result_text:
                    action_desc += "\n  结果: %s" % result_text

                action_lines.append(action_desc)

        actions_text = "\n".join(action_lines)

    return RESPONSE_PROMPT % {
        "user_message": user_message,
        "history": history_text,
        "plan": plan,
        "actions_text": actions_text
    }