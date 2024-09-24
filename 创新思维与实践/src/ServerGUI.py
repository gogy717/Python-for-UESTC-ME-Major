from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QToolButton)
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from src.Tcp_server import TcpServer
from src.line_segment import *
import time

class ServerGUI(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.mode = 'localhost'  # 初始模式
        self.host = '127.0.0.1'
        self.port = 80

        self.init_ui()

        # 连接信号和槽
        self.log_signal.connect(self.update_log)

        self.server_thread = None
        
        # 消息
        self.message = "No message yet"
        
        # 加载样式表
        self.apply_styles()
        
    def init_ui(self):
        self.setWindowTitle("TCP 服务器")
        self.resize(600, 550)

        # 模式显示标签
        self.mode_label = QLabel(f"当前模式: {self.mode}")

        # 模式切换按钮，改为较小的 QToolButton
        self.toggle_mode_button = QToolButton()
        self.toggle_mode_button.setText("局域网模式")
        self.toggle_mode_button.setStyleSheet("QToolButton \
                                              { min-width: 100px; min-height: 30px; \
                                              font-size: 12px; }")

        self.toggle_mode_button.clicked.connect(self.toggle_mode)

        # 端口号输入
        self.port_label = QLabel("端口号:")
        self.port_entry = QLineEdit(str(self.port))
        self.set_port_button = QPushButton("设置端口号")
        self.set_port_button.clicked.connect(self.set_port)

        # 启动和停止按钮放在同一行
        self.start_button = QPushButton("启动服务器")
        self.start_button.clicked.connect(self.start_server)
        self.stop_button = QPushButton("停止服务器")
        self.stop_button.clicked.connect(self.stop_server)
        self.stop_button.setEnabled(False)
        
        # 创建按钮水平布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # 消息发送区域
        self.message_label = QLabel("消息:")
        self.message_entry = QLineEdit()
        self.send_button = QPushButton("发送消息")
        self.send_button.clicked.connect(self.send_message)

        # 开始图像处理
        self.run_button = QPushButton("开始图像处理")
        self.run_button.clicked.connect(self.run_gui)

        # 日志显示区域
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        # 布局设置
        layout = QVBoxLayout()
        layout.addWidget(self.mode_label)
        layout.addWidget(self.toggle_mode_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_entry)
        layout.addWidget(self.set_port_button)
        layout.addLayout(button_layout)  # 启动和停止按钮同一行
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_entry)
        layout.addWidget(self.send_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.log_area)

        self.setLayout(layout)

    def toggle_mode(self):
        if self.mode == 'localhost':
            self.mode = '局域网'
            self.host = '0.0.0.0'
            self.toggle_mode_button.setText("本地模式")
            self.log(f"已切换到局域网模式，服务器将监听所有网络接口。")
        else:
            self.mode = 'localhost'
            self.host = '127.0.0.1'
            self.toggle_mode_button.setText("局域网模式")
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

    def send_message(self):
        message = self.message_entry.text()
        if not message:
            self.log("消息不能为空。")
            return
        if self.server_thread:
            self.server_thread.server.send_message(message)
            self.log(f"已发送消息: {message}")
        else:
            self.log("请先启动服务器。")
    
    def run_gui(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                cv2.imwrite("images/line1.jpg", frame)
                break
        cap.release()
        time.sleep(1)
        line_image = image("images/line1.jpg")
        line_image.run()
        step = 10
        targets = line_image.targets
        data: Dict[Tuple[int, int], float] = {}
        for i in range(0, len(targets), step):
            data[list(targets.keys())[i]] = list(targets.values())[i]
        if len(targets) % step > step // 2:
            data[list(targets.keys())[-1]] = list(targets.values())[-1]
        line_image.draw_points(data)
        data_string: str = "a"
        for key, value in data.items():
            data_string += (str(key[0]) + ',')
            data_string += (str(key[1]) + ',')
            value = np.arctan(value)
            value = np.degrees(value)
            value = round(value, 2)
            data_string += (str(value) + ',')
        self.server_thread.server.send_message(data_string)


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
    
    def apply_styles(self):
        # 读取样式表文件并应用
        with open("src/style.qss", "r") as file:
            stylesheet = file.read()
            self.setStyleSheet(stylesheet)


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

if __name__ == "__main__":
    app = QApplication([])
    gui = ServerGUI()
    gui.show()
    app.exec_()