import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
from .Tcp_server import TcpServer


class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("TCP 服务器")
        master.geometry("600x450")  # 增加高度以容纳新的控件

        # 创建端口号输入框
        self.port_label = tk.Label(master, text="端口号:")
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, "12345")  # 默认端口号
        self.port_entry.pack(pady=5)

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

    def set_port(self):
        """
        设置服务器的端口号
        """
        port_str = self.port_entry.get()
        try:
            port = int(port_str)
            if 0 <= port <= 65535:
                self.port = port
                return True
            else:
                self.log("端口号必须在 0 到 65535 之间。")
                return False
        except ValueError:
            self.log("请输入有效的端口号。")
            return False

    def start_server(self):
        if not self.set_port():
            return  # 如果端口号无效，不启动服务器

        # 禁用启动按钮，启用停止按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # 创建并启动服务器线程，使用指定的端口号
        self.server = TcpServer(port=self.port, gui=self)
        self.server_thread = threading.Thread(target=self.server.start_server)
        self.server_thread.start()

    def stop_server(self):
        # 启用启动按钮，禁用停止按钮
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

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

