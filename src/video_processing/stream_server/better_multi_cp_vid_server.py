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
        rpi_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rpi_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        rpi_sock.bind((host, port))
        rpi_sock.listen(10)
        print("[*] Server listening on port")
        rpi_client_conn = rpi_sock.accept()[0].makefile('rb')
        print("Rpi connected")

        #USER 1
        gui1_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        gui1_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        gui1_sock.bind((host, 6667))
        gui1_sock.listen(10)
        print("[*] Server listening on port")
        gui1_conn = gui1_sock.accept()[0].makefile('rb')
        print("GUI 1 connected")

        while True:    
            print("running")
            image_len = struct.unpack('<L', rpi_client_conn.read(struct.calcsize('<L')))[0] #unpacks from buffer of bytes
            print(image_len)
            #image_len is a bytes like object to be written in to the image stream 
            if not image_len:
                print("no image stream was unpacked")
                break
            image_stream = io.BytesIO()
            image_stream.write(rpi_client_conn.read(image_len))
            gui1_conn.write(struct.pack('<L',image_stream.tell())) #reports the size of the entire stream at current point.. end of stream?
            gui1_conn.flush() #flush content to a file...
            image_stream.seek(0) #change stream position to start of stream, 0
            gui1_conn.write(image_stream.read())
            image_stream.truncate()
        gui1_conn.write(struct.pack('<L',0))
    except:
        rpi_client_conn.close()
        rpi_sock.close()
        gui1_conn.close()
        gui1_sock.close()
    finally:
        gui1_conn.close()
        gui1_sock.close()
        rpi_client_conn.close()
        rpi_sock.close()
    

if __name__ == "__main__":
    main()
