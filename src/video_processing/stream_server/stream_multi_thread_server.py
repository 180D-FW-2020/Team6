#!usr/bin/python
import io
from PIL import Image
import matplotlib.pyplot as pl
#import thread as thread
from _thread import *
import socket
import sys

def clientthread(conn):
    buffer=""
    while True:
        data = conn.recv(8192)
        #buf = data.decode('ASCII')
        print(data)
    #conn.sendall(reply)
    conn.close()

def main():
    try:
        host = '0.0.0.0'
        port = 6666
        tot_socket = 2
        list_sock = []
        for i in range(tot_socket):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            s.bind((host, port+i))
            s.listen(10)
            list_sock.append(s)
            print("[*] Server listening on port")

        while 1:
            for j in range(len(list_sock)):
                conn, addr = list_sock[j].accept()
                print('[*] Connected with ' + addr[0] + ':' + str(addr[1]))

                if j == 0:
                    print("RPI connected")
                elif j == 1:
                    print("GUI connected")
            #both sockets are now connected
            rpi_cient_socket = list_sock[0]
            gui_client_socket = list_sock[1]

            data = rpi_cient_socket.recv(8192)
            gui_client_socket.sendall(data)
                
        s.close()

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
