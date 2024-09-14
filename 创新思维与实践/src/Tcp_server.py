import socket
import threading
try:
    from ServerGUI import *
except ImportError:
    from .ServerGUI import *

class TcpServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.is_running = False
        self.client_threads = []

    def start_server(self):
        # 初始化服务器套接字
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.is_running = True
            print(f'服务器已启动，正在监听 {self.host}:{self.port}')
        except Exception as e:
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
                print(f'客户端已连接: {addr}')
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                client_thread.start()
                self.client_threads.append(client_thread)
            except Exception as e:
                print(f'接受客户端连接时出错: {e}')

    def handle_client(self, client_socket, addr):
        while self.is_running:
            try:
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f'收到来自 {addr} 的数据: {message}')
                    # 处理接收到的数据，可以根据需要修改
                    response = f'服务器已收到您的消息: {message}'
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    # 客户端断开连接
                    print(f'客户端 {addr} 已断开连接')
                    break
            except Exception as e:
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
        print('服务器已停止')

# 示例使用
if __name__ == '__main__':
    server = TcpServer(host='127.0.0.1', port=8080)
    try:
        server.start_server()
        while True:
            pass  # 保持主线程运行
    except KeyboardInterrupt:
        server.stop_server()