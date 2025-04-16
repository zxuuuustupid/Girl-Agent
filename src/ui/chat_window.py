from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QTextEdit, QLineEdit, QPushButton, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QIcon, QPixmap
import asyncio
from agent.base import Agent

class ChatThread(QThread):
    response_received = pyqtSignal(str)
    
    def __init__(self, agent, message):
        super().__init__()
        self.agent = agent
        self.message = message
        
    def run(self):
        response = asyncio.run(self.agent.process_input(self.message))
        self.response_received.emit(response)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agent = Agent()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('AI 女友')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTextEdit {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
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
        
        # 显示欢迎消息
        self.chat_display.append('AI: 你好！我是你的AI女友，很高兴见到你！')
        
    def send_message(self):
        message = self.message_input.text().strip()
        if not message:
            return
            
        # 显示用户消息
        self.chat_display.append(f'你: {message}')
        self.message_input.clear()
        
        # 创建并启动聊天线程
        self.chat_thread = ChatThread(self.agent, message)
        self.chat_thread.response_received.connect(self.show_response)
        self.chat_thread.start()
        
    def show_response(self, response):
        self.chat_display.append(f'AI: {response}')
        # 滚动到底部
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        ) 