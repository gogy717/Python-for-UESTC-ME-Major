# server_gui.py
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout)
from PyQt5.QtCore import pyqtSignal, QThread
from src.Tcp_server import TcpServer

class ServerGUI(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.mode = 'localhost'  # 初始模式
        self.host = '127.0.0.1'
        self.port = 12345

        self.init_ui()

        # 连接信号和槽
        self.log_signal.connect(self.update_log)

        self.server_thread = None

    def init_ui(self):
        self.setWindowTitle("TCP 服务器")
        self.resize(600, 550)

        # 模式显示标签
        self.mode_label = QLabel(f"当前模式: {self.mode}")

        # 模式切换按钮
        self.toggle_mode_button = QPushButton("切换到局域网模式")
        self.toggle_mode_button.clicked.connect(self.toggle_mode)

        # 端口号输入
        self.port_label = QLabel("端口号:")
        self.port_entry = QLineEdit(str(self.port))
        self.set_port_button = QPushButton("设置端口号")
        self.set_port_button.clicked.connect(self.set_port)

        # 启动和停止按钮
        self.start_button = QPushButton("启动服务器")
        self.start_button.clicked.connect(self.start_server)
        self.stop_button = QPushButton("停止服务器")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)

        # 日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.mode_label)
        layout.addWidget(self.toggle_mode_button)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_entry)
        layout.addWidget(self.set_port_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def toggle_mode(self):
        if self.mode == 'localhost':
            self.mode = '局域网'
            self.host = '0.0.0.0'
            self.toggle_mode_button.setText("切换到本地模式")
            self.log(f"已切换到局域网模式，服务器将监听所有网络接口。")
        else:
            self.mode = 'localhost'
            self.host = '127.0.0.1'
            self.toggle_mode_button.setText("切换到局域网模式")
            self.log(f"已切换到本地模式，服务器将仅监听本地接口。")
        self.mode_label.setText(f"当前模式: {self.mode}")

    def set_port(self):
        port_str = self.port_entry.text()
        try:
            port = int(port_str)
            if 0 <= port <= 65535:
                self.port = port
                self.log(f"端口号已设置为 {self.port}")
                return True
            else:
                self.log("端口号必须在 0 到 65535 之间。")
                return False
        except ValueError:
            self.log("请输入有效的端口号。")
            return False

    def start_server(self):
        if not hasattr(self, 'port'):
            self.log("请先设置端口号。")
            return

        # 禁用启动按钮和模式切换按钮，启用停止按钮
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.toggle_mode_button.setEnabled(False)

        # 创建并启动服务器线程
        self.server_thread = ServerThread(host=self.host, port=self.port)
        self.server_thread.log_signal.connect(self.log_signal)
        self.server_thread.start()

    def stop_server(self):
        # 启用启动按钮和模式切换按钮，禁用停止按钮
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.toggle_mode_button.setEnabled(True)

        # 停止服务器线程
        if self.server_thread:
            self.server_thread.stop()
            self.server_thread = None

    def log(self, message):
        self.log_signal.emit(message)

    def update_log(self, message):
        self.log_area.append(message)
        self.log_area.ensureCursorVisible()

class ServerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server = None

    def run(self):
        self.server = TcpServer(host=self.host, port=self.port, log_callback=self.log)
        self.server.start_server()

    def log(self, message):
        self.log_signal.emit(message)

    def stop(self):
        if self.server:
            self.server.stop_server()
        self.quit()
        self.wait()
        