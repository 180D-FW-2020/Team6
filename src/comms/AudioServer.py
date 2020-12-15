import pyaudio
import socket

BUFFERSIZE = 1024

class AudioServer:
    def __init__(self, ip="127.0.0.1", port=3009):
        self.ip = ip 
        self.port = port
        self.server_conn = None
        self.socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
    def start(self):
        print("Listening for connection")
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        self.server_conn, addr = self.socket.accept()
        print(f"Accepted connection from {addr} on port {self.port}")
    
    def stop(self):
        self.server_conn.shutdown(socket.SHUT_RDWR)
        self.server_conn.close()

    def send(self, msg):       
        self.server_conn.send(msg)
