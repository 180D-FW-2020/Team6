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

        gui_sock = socket.socket()
        gui_sock.connect(('172.91.89.246',6667))#connects to gui laptop IP
        print("[*] Client listening on port")
        gui_conn = gui_sock.makefile('wb')
        print("Gui connected")

        while True:    
            print("running")
            image_len = struct.unpack('<L', rpi_client_conn.read(struct.calcsize('<L')))[0] #unpacks from buffer of bytes
            print(image_len)
            #image_len is a bytes like object to be written in to the image stream 
            if not image_len:
                print("no image stream was unpacked")
                break
            image_stream = io.BytesIO() #stream of bytes
            image_stream.write(rpi_client_conn.read(image_len))  #writes the byte like object from rpi to the raw stream
            
            #image = Image.open(image_stream) #open the PIL image


            gui_conn.write(struct.pack('<L',image_stream.tell())) #reports the size of the entire stream at current point.. end of stream?
            gui_conn.flush() #flush content to a file...
            image_stream.seek(0) #change stream position to start of stream, 0
            gui_conn.write(image_stream.read())
            image_stream.seek(0)
            image_stream.truncate()
        gui_conn.write(struct.pack('<L',0))
        
    finally:
        gui_conn.close()
        gui_sock.close()
        rpi_client_conn.close()
        rpi_sock.close()
    

if __name__ == "__main__":
    main()
