import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import socket
import time

from src.Tcp_server import TcpServer
from src.ServerGUI import ServerGUI


if __name__ == '__main__':
    root = tk.Tk()
    gui = ServerGUI(root)
    root.mainloop()
    
    
    