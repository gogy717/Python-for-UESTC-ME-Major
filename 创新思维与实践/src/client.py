import socket
import threading

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                print("收到服务器消息:", data.decode('utf-8'))
            else:
                break
        except:
            break

def main():
    host = '127.0.0.1'  # 替换为服务器的IP地址
    port = 12345  # 端口号

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
        print("已连接到服务器")
    except Exception as e:
        print(f"无法连接到服务器: {e}")
        return

    # 启动接收消息的线程
    recv_thread = threading.Thread(target=receive_messages, args=(sock,))
    recv_thread.start()

    # 主线程用于发送消息给服务器
    while True:
        message = input()
        if message.lower() == 'exit':
            break
        try:
            sock.sendall(message.encode('utf-8'))
        except:
            break

    sock.close()

if __name__ == '__main__':
    main()