import json
import socket

# Socket buffer
BUFFER = 2048

class DBInterface():
    def __init__(self, ip="3.19.57.159", port=3333):
        self.ip = ip
        self.port = port
    
    def _start(self):
        self.ip = self.ip
        self.port = self.port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.ip, self.port))

    def _close(self):
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
        except:
            pass
        self.conn.close()

    def _send(self, str_json):
        # Connect to server.
        self._start()
        str_json = str_json.encode()
        self.conn.send(str_json)

        # Server response
        raw = self.conn.recv(BUFFER)
        raw = raw.decode()

        # Close server connection.
        self._close()

        return raw
    
    def register(self, user, email, pswd):
        # Register request
        req = f'{{"func":"register", "user":"{user}", "email":"{email}", "pswd":"{pswd}"}}'
        raw = self._send(req)

        return raw

    def login(self, user, pswd):
        # Login request
        req = f'{{"func":"login", "user":"{user}", "pswd":"{pswd}"}}'
        raw = self._send(req)

        return raw