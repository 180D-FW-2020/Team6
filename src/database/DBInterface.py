import json
import socket

# Socket buffer
BUFFER = 2048

class DBInterface():
    def __init__(self, ip="3.19.57.159", port=3333):
        self.ip = ip
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def _start(self):
        self.conn.connect((self.ip, self.port))

    def _close(self):
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.conn.close()

    def login(self, user, pswd):
        self._start()

        # Login request
        cred = f'{{"func":"login", "user":"{user}", "pswd":"{pswd}"}}'
        cred = cred.encode()
        self.conn.send(cred)

        # Server response
        raw = self.conn.recv(BUFFER)
        raw = raw.decode()

        self._close()

        return raw