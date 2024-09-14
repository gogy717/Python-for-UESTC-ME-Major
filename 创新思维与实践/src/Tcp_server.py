import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import queue
from .ipGet import get_local_ip

class TcpServer:
    def __init__(self, host='127.0.0.1', port=12345, gui=None):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.client_threads = []
        self.gui = gui  # 引用 GUI 对象

    def start_server(self):
        # 初始化服务器套接字
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_running = True
            if self.gui:
                self.gui.log(f'服务器已启动，正在监听 {self.host}:{self.port}')
                if self.gui.mode == 'localhost':
                    self.gui.log("当前模式: 本地模式")
                else:
                    self.gui.log("当前模式: 局域网模式")
                    self.gui.log(f"本机 IP 地址: {get_local_ip()}")
            else:
                print(f'服务器已启动，正在监听 {self.host}:{self.port}')
        except Exception as e:
            if self.gui:
                self.gui.log(f'服务器启动失败: {e}')
            else:
                print(f'服务器启动失败: {e}')
            self.stop_server()
            return

        # 开始接受客户端连接的线程
        accept_thread = threading.Thread(target=self.accept_clients)
        accept_thread.start()

    def accept_clients(self):
        while self.is_running:
            try:
                client_socket, addr = self.server_socket.accept()
                if self.gui:
                    self.gui.log(f'客户端已连接: {addr}')
                else:
                    print(f'客户端已连接: {addr}')
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()
                self.client_threads.append(client_thread)
            except Exception as e:
                if self.gui:
                    self.gui.log(f'接受客户端连接时出错: {e}')
                else:
                    print(f'接受客户端连接时出错: {e}')

    def handle_client(self, client_socket, addr):
        while self.is_running:
            try:
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    if self.gui:
                        self.gui.log(f'收到来自 {addr} 的数据: {message}')
                    else:
                        print(f'收到来自 {addr} 的数据: {message}')
                    # 处理接收到的数据，可以根据需要修改
                    response = f'服务器已收到您的消息: {message}'
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    # 客户端断开连接
                    if self.gui:
                        self.gui.log(f'客户端 {addr} 已断开连接')
                    else:
                        print(f'客户端 {addr} 已断开连接')
                    break
            except Exception as e:
                if self.gui:
                    self.gui.log(f'处理客户端 {addr} 数据时出错: {e}')
                else:
                    print(f'处理客户端 {addr} 数据时出错: {e}')
                break
        client_socket.close()

    def stop_server(self):
        self.is_running = False
        # 关闭所有客户端连接
        for client_thread in self.client_threads:
            if client_thread.is_alive():
                client_socket = client_thread._args[0]
                client_socket.close()
        # 关闭服务器套接字
        if self.server_socket:
            self.server_socket.close()
        if self.gui:
            self.gui.log('服务器已停止')
        else:
            print('服务器已停止')
            
            