# src/main_gui.py

import sys
import os
import asyncio
import io
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QTextCursor, QColor, QTextCharFormat, QIcon

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

from agent.base import Agent

class OutputRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = io.StringIO()
        
    def write(self, text):
        self.buffer.write(text)
        if text.startswith("AI: "):
            text = text[4:]
        self.text_widget.append_message('Lamia', text.strip())
        
    def flush(self):
        pass

class ChatThread(QThread):
    response_received = pyqtSignal(str)
    
    def __init__(self, agent, message):
        super().__init__()
        self.agent = agent
        self.message = message
        
    def run(self):
        try:
            # 直接调用 process_input 并等待结果
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.agent.process_input(self.message))
            loop.close()
            self.response_received.emit(response)
        except Exception as e:
            print(f"Error in chat thread: {e}")
            self.response_received.emit(f"发生错误: {str(e)}")

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('GirlAgent')
        self.setWindowIcon(QIcon('assets/heart.png'))
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fff0f5;
            }
            QLabel#title {
                font-size: 24px;
                color: #ff69b4;
                font-weight: bold;
                padding: 10px;
            }
            QTextEdit {
                background-color: #fff0f5;
                border: 2px solid #ff69b4;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit {
                background-color: white;
                border: 2px solid #ff69b4;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                color: black;
            }
            QPushButton {
                background-color: #ff69b4;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff1493;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标题栏
        title_label = QLabel('❤️ 你的电子女友 ❤️')
        title_label.setObjectName('title')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 创建聊天显示区域
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont('Microsoft YaHei', 12))
        main_layout.addWidget(self.chat_display)
        
        # 创建输入区域
        input_layout = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText('输入消息...')
        self.message_input.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.message_input)
        
        send_button = QPushButton('发送')
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)
        
        main_layout.addLayout(input_layout)
        
        # 设置输出重定向
        self.output_redirector = OutputRedirector(self)
        sys.stdout = self.output_redirector
        
        # 显示欢迎消息
        self.append_message('Lamia', '你好！我是你的AI女友，很高兴见到你！')
        
    def append_message(self, sender, message):
        if not message.strip():
            return
            
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # 设置消息格式
        format = QTextCharFormat()
        if sender == '你':
            format.setForeground(QColor('#ff69b4'))  # 粉色
            cursor.insertText(f'\n{sender}: ', format)
            format.setForeground(QColor('#000000'))  # 黑色
            cursor.insertText(message, format)
        else:
            format.setForeground(QColor('#4169e1'))  # 蓝色
            cursor.insertText(f'\n{sender}: ', format)
            format.setForeground(QColor('#000000'))  # 黑色
            cursor.insertText(message, format)
        
        # 滚动到底部
        self.chat_display.setTextCursor(cursor)
        self.chat_display.ensureCursorVisible()
        
    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return
            
        # 检查退出命令
        if message.lower() in ['exit', 'quit', '退出']:
            self.append_message('Lamia', '再见啦！期待下次见面哦～')
            self.close()
            return
            
        # 显示用户消息
        self.append_message('你', message)
        self.message_input.clear()
        
        # 创建并启动聊天线程
        self.chat_thread = ChatThread(self.agent, message)
        self.chat_thread.response_received.connect(self.show_response)
        self.chat_thread.start()
        
    def show_response(self, response):
        if response:  # 确保有响应才显示
            if response.startswith("Lamia: "):
                response = response[4:]
            self.append_message('Lamia', response)

def main():
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 