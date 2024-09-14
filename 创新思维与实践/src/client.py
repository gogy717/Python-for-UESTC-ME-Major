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

# 示例使用
if __name__ == '__main__':
    client = TcpClient(host='127.0.0.1', port=12345)
    client.connect()
    client.send('Hello, Server!')
    client.receive()
    client.close()
