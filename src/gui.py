import sys
import os
import asyncio
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton,
                             QLabel, QScrollArea)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon, QTextCursor

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from agent.base import Agent


class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.setup_ui()
        self.setup_styles()
        self.setWindowTitle("你的浪漫女友")

        # 设置窗口图标
        self.setWindowIcon(QIcon(os.path.join(ROOT_DIR, "assets", "heart.png")))

        # 启动欢迎消息的异步任务
        self.start_welcome_message_task()

    def setup_ui(self):
        # 主窗口设置
        self.setMinimumSize(800, 600)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题
        title_label = QLabel("💖 你的浪漫女友 💖")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #ff6b9e;
            margin-bottom: 20px;
        """)
        main_layout.addWidget(title_label)

        # 聊天区域
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("""
            QTextEdit {
                background-color: #fff0f5;
                border: 2px solid #ffc0cb;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                color: #5a3d5a;
            }
        """)

        # 添加滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.chat_area)
        main_layout.addWidget(scroll_area, 1)

        # 输入区域
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("输入你想说的话...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #ffc0cb;
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 16px;
                color: #5a3d5a;
            }
        """)
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field, 1)

        send_button = QPushButton("发送")
        send_button.setStyleSheet("""
            QPushButton {
                background-color: #ff6b9e;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff4785;
            }
        """)
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        main_layout.addLayout(input_layout)

        # 底部退出按钮
        exit_button = QPushButton("退出聊天")
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #dcdcdc;
                color: #5a3d5a;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
        """)
        exit_button.clicked.connect(self.close)
        main_layout.addWidget(exit_button, 0, Qt.AlignRight)

    def setup_styles(self):
        # 设置窗口背景
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fff0f5;
            }
        """)

    async def show_welcome_message(self):
        welcome_messages = [
            "嗨，亲爱的~ ❤️",
            "今天过得怎么样呀？",
            "我好想你哦~",
            "有什么想和我分享的吗？"
        ]

        for msg in welcome_messages:
            self.append_message("女友", msg, is_user=False)
            QApplication.processEvents()  # 确保UI更新
            await asyncio.sleep(0.5)

    def start_welcome_message_task(self):
        # 启动异步任务
        loop = asyncio.get_event_loop()
        loop.create_task(self.show_welcome_message())

    def append_message(self, sender, message, is_user=True):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.End)

        if is_user:
            # 用户消息样式（靠右）
            cursor.insertHtml(f"""
                <div style="margin: 10px; text-align: right;">
                    <div style="background-color: #fff0f5; color: #5a3d5a; border-radius: 15px; padding: 10px 15px; display: inline-block; max-width: 70%; margin-left: 30%;">
                        <b>你:</b> {message}<br>
                    </div>
                </div>
            """)
        else:
            # 女友消息样式（靠左）
            cursor.insertHtml(f"""
                <div style="margin: 10px; text-align: left;">
                    <div style="background-color: #fff0f5; color: #5a3d5a; border-radius: 15px; padding: 10px 15px; display: inline-block; max-width: 70%; margin-right: 30%;">
                        <b>{sender}:</b> {message}<br>
                    </div>
                </div>
            """)

        # 自动滚动到底部
        self.chat_area.ensureCursorVisible()

    async def get_agent_response(self, message):
        return await self.agent.process_input(user_message=message)

    def send_message(self):
        message = self.input_field.text().strip()
        if not message:
            return

        self.append_message("你", message, is_user=True)
        self.input_field.clear()

        # 使用QTimer来异步处理响应
        QTimer.singleShot(100, lambda: self.process_response(message))

    def process_response(self, message):
        # 创建一个新的事件循环来处理异步响应
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            response = loop.run_until_complete(self.get_agent_response(message))
            print(f"Response from agent: {response}")  # 调试信息
            self.append_message("女友", str(response), is_user=False)  # 直接显示 response
        finally:
            loop.close()


def main():
    app = QApplication(sys.argv)

    # 设置应用程序字体
    font = QFont()
    font.setFamily("Microsoft YaHei" if sys.platform == "win32" else "PingFang SC")
    font.setPointSize(12)
    app.setFont(font)

    window = ChatWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()