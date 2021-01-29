import pyaudio
import socket

class MicClient:
    def __init__(self, ip="3.140.200.49", port=5001):
        self.ip = ip 
        self.port = port
        self.client_conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)   

    def start(self):
        self.client_conn.connect((self.ip, self.port))
        print(f"Connected to {self.ip} on port {self.port}")
    
    def stop(self):
        self.client_conn.shutdown(socket.SHUT_RDWR)
        self.client_conn.close()

    def send(self, msg):
        self.client_conn.send(msg)
