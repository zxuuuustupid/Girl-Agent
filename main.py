import sys
import os

# 把 src 加入模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)

# 调用 src/main.py 中的 main 函数
from src.main import main  # 注意：src/main.py 中应有 def main()
main()
