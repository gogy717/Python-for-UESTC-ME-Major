import socket

def get_local_ip():
    # 创建一个UDP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到局域网中的某个地址（例如路由器地址），但不需要真的发送数据
        s.connect(('8.8.8.8', 80))
        # 获取分配的IP地址
        local_ip = s.getsockname()[0]
    finally:
        # 关闭套接字
        s.close()
    return local_ip

# 获取本机的局域网IP地址
print("Local IP address:", get_local_ip())