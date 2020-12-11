#!usr/bin/python
import io
from PIL import Image
import matplotlib.pyplot as pl
#import thread as thread
from _thread import *
import socket
import sys

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
        list_conn = []
        for j in range(len(list_sock)):
            conn, addr = list_sock[j].accept()
            print('[*] Connected with ' + addr[0] + ':' + str(addr[1]))
            list_conn.append(conn)
            if j == 0:
                print("RPI connected")
                    
            elif j == 1:
                print("GUI connected")
            #print(list_conn[0])
            #print(list_conn[1])
            #both sockets are now connected
        rpi_client_conn = list_conn[0]
        gui_client_conn = list_conn[1]
        while True:    
            data = rpi_client_conn.recv(8192)
            gui_client_conn.send(data)
            print("sending data")
        
        for j in range(len(list_sock)): #changed
            list_sock[j].close()

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
