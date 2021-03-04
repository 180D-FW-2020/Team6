import json
import requests
import socket
import webbrowser

BUFFER = 2048

class S3Interface():
    #3.17.11.232
    def __init__(self, ip="3.17.11.232", port=5674):
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
    
    def get_all(self):
        # GET all request.
        req = '{"func":"get_all"}'
        raw = self._send(req)

        return json.loads(raw)

    def get_one(self, name):
        # GET one request.
        req = f'{{"func":"get_one", "name":"{name}"}}'
        raw = self._send(req)

        return json.loads(raw)
    
    def post_one(self, name, pathname):
        # POST one request.
        req = f'{{"func":"post_one", "name":"{name}"}}'
        raw = self._send(req)
        res = json.loads(raw)
        
        if "res" in res:
            response = res["res"]

            try:
                with open(pathname, 'rb') as f:
                    files = {'file': (name, f)}
                    http_response = requests.post(response['url'], 
                                                  data=response['fields'], 
                                                  files=files)
            except Exception as err:
                res["status"] = False
                res["err"] = str(err)

            res.pop("res", None)

        return res
