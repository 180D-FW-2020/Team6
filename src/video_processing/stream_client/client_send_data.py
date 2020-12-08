import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('3.15.16.101',6666)
print("connecting to server")
sock.connect(server_address)

try:
    message = "message from rpi"
    byte_m = message.encode('ASCII')
    while True:
        print("sending message ")
        sock.sendall(byte_m)
finally:
	print("closing socket")
	sock.close()
