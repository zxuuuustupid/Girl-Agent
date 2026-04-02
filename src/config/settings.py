import os

# 尝试加载 .env 文件（如果安装了 python-dotenv）
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

MEMORY_SIZE = 20

# 从环境变量读取，无则用空字符串（空 key 会让调用失败并给出明确提示）
DEEPSEEK_SETTINGS = {
    "api_key": os.getenv("DEEPSEEK_API_KEY", ""),
    "api_base": os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com"),
    "model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
}

ZHIPU_SETTINGS = {
    "api_key": os.getenv("ZHIPU_API_KEY", ""),
    "api_base": os.getenv("ZHIPU_API_BASE", "https://open.bigmodel.cn/api/paas/v4/"),
    "model": os.getenv("ZHIPU_MODEL", "glm-4-flash"),
}

ZHIZENG_SETTINGS = {
    "api_key": os.getenv("ZHIZENG_API_KEY", ""),
    "api_base": os.getenv("ZHIZENG_API_BASE", "https://api.zhizengzeng.com/v1"),
    "model": os.getenv("ZHIZENG_MODEL", "deepseek-chat"),
}

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_API_BASE = os.getenv("MINIMAX_API_BASE", "https://api.minimaxi.com/anthropic")
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "MiniMax-M2.7")

OPENROUTER_SETTINGS = {
    "api_key": os.getenv("OPENROUTER_API_KEY", ""),
    "api_base": os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1"),
    "model": os.getenv("OPENROUTER_MODEL", ""),
}

# 选择使用的LLM服务（从 provider.py 导入）
from .provider import LLM_PROVIDER

AGENT_SETTINGS = {
    "name": "Megumi",
    "age": 19,
    "gender": "女",
    "occupation": "学生",
    "personality":"slapper"
}
