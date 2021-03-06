import pyaudio
import socket

class MicClient:
    def __init__(self, ip="18.189.21.182", port=3356):
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
