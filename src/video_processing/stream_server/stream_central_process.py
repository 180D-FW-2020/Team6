#!usr/bin/python
import io
from PIL import Image
import struct
import matplotlib.pyplot as pl
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

            if j == 0: #rpi connection
                conn = list_sock[j].accept()[0].makefile('rb')
            if j == 1: #gui connection
                conn = list_sock[j].accept()[0].makefile('wb')

            #print('[*] Connected with ' + addr[0] + ':' + str(addr[1]))
            list_conn.append(conn)
            if j == 0:
                print("RPI connected")
                    
            elif j == 1:
                print("GUI connected")    
        
        #both sockets are now connected
        rpi_client_conn = list_conn[0]
        gui_client_conn = list_conn[1]
        
        while True:    
            print("running")
            image_len = struct.unpack('<L', rpi_client_conn.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            image_stream = io.BytesIO()
            image_stream.write(rpi_client_conn.read(image_len))
            image_stream.seek(0)
            image = Image.open(image_stream)


            #gui_client_conn.write(struct.pack('<L',image.tell()))
            gui_client_conn.send(image)
            print("sent to gui")
            image.seek(0)

        for j in range(len(list_sock)): #changed
            list_sock[j].close()

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
