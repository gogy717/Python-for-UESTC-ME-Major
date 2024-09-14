import socket
import threading
import time
import serial
import numpy as np

class TcpClient():
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.client_socket = None
        self.is_connected = False

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.is_connected = True
            print(f'已连接到服务器 {self.host}:{self.port}')
        except Exception as e:
            print(f'连接失败: {e}')

    def send(self, data):
        if self.is_connected:
            try:
                self.client_socket.sendall(data.encode('utf-8'))
                print(f'发送数据: {data}')
            except Exception as e:
                print(f'发送失败: {e}')
        else:
            print('未连接到服务器')

    def receive(self):
        if self.is_connected:
            try:
                response = self.client_socket.recv(1024).decode('utf-8')
                print(f'接收数据: {response}')
                return response
            except Exception as e:
                print(f'接收失败: {e}')
        else:
            print('未连接到服务器')

    def close(self):
        if self.is_connected:
            self.client_socket.close()
            self.is_connected = False
            print('连接已关闭')
            
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
    
    
# 示例使用
if __name__ == '__main__':
    client = TcpClient(host='127.0.0.1', port=8080)
    client.connect()
    client.send('Hello, Server!')
    client.receive()
    client.close()
