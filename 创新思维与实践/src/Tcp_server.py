import socket
import threading
import time
import serial
import numpy as np

from typing import List, Tuple, Dict


class Tcp_server:
    def __init__(self, host: str = "172.168.0.2"):
        self.host = host
        self.port = 12345
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.client, self.addr = self.server.accept()
        self.ser = serial.Serial("/dev/ttyUSB0", 9600)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.write(b"Hello from Python!")
        self.ser.flush()
        self.ser.close()
    


