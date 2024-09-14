import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
from .Tcp_server import TcpServer


class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("TCP 服务器")
        master.geometry("600x550")  # 增加高度以容纳新的控件

        # 初始化地址和端口号
        self.mode = 'localhost'  # 初始模式为本地模式
        self.host = '127.0.0.1'  # 默认绑定地址
        self.port = 12345  # 默认端口号

        # 创建模式显示标签
        self.mode_label = tk.Label(master, text=f"当前模式: {self.mode}")
        self.mode_label.pack(pady=5)

        # 创建模式切换按钮
        self.toggle_mode_button = tk.Button(master, text="切换到局域网模式", command=self.toggle_mode)
        self.toggle_mode_button.pack(pady=5)

        # 创建端口号输入框
        self.port_label = tk.Label(master, text="端口号:")
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, str(self.port))  # 默认端口号
        self.port_entry.pack(pady=5)

        # 创建端口号设置按钮
        self.set_port_button = tk.Button(master, text="设置端口号", command=self.set_port)
        self.set_port_button.pack(pady=5)

        # 创建启动和停止按钮
        self.start_button = tk.Button(master, text="启动服务器", command=self.start_server)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="停止服务器", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # 创建日志显示区域
        self.log_area = scrolledtext.ScrolledText(master, state='disabled', width=70, height=20)
        self.log_area.pack(pady=5)

        # 用于在子线程中安全地更新日志
        self.log_queue = queue.Queue()
        self.update_log()

    def toggle_mode(self):
        if self.mode == 'localhost':
            self.mode = '局域网'
            self.host = '0.0.0.0'  # 监听所有网络接口
            self.toggle_mode_button.config(text="切换到本地模式")
            self.log("已切换到局域网模式，服务器将监听所有网络接口。")
        else:
            self.mode = 'localhost'
            self.host = '127.0.0.1'  # 仅监听本地回环接口
            self.toggle_mode_button.config(text="切换到局域网模式")
            self.log("已切换到本地模式，服务器将仅监听本地接口。")
        self.mode_label.config(text=f"当前模式: {self.mode}")

    def set_port(self):
        """
        设置服务器的端口号
        """
        port_str = self.port_entry.get()
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
        # 检查是否已设置端口号
        if not hasattr(self, 'port'):
            self.log("请先设置端口号。")
            return

        # 禁用启动按钮和模式切换按钮，启用停止按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.toggle_mode_button.config(state=tk.DISABLED)

        # 创建并启动服务器线程，使用指定的地址和端口号
        self.server = TcpServer(host=self.host, port=self.port, gui=self)
        self.server_thread = threading.Thread(target=self.server.start_server)
        self.server_thread.start()

    def stop_server(self):
        # 启用启动按钮和模式切换按钮，禁用停止按钮
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.toggle_mode_button.config(state=tk.NORMAL)

        # 停止服务器
        if hasattr(self, 'server'):
            self.server.stop_server()

    def log(self, message):
        # 将日志消息放入队列
        self.log_queue.put(message)

    def update_log(self):
        # 从队列中获取日志消息并更新日志区域
        while not self.log_queue.empty():
            message = self.log_queue.get()
            self.log_area.config(state='normal')
            self.log_area.insert(tk.END, message + '\n')
            self.log_area.see(tk.END)
            self.log_area.config(state='disabled')
        # 定时调用自身，以持续更新日志
        self.master.after(100, self.update_log)
        
