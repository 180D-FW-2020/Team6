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

        #User 1
        gui_sock = socket.socket()
        gui_sock.connect(('172.91.89.246',6667))#connects to gui laptop IP of User 1
        print("[*] Client_user 1 listening on port") #Henry's Laptop
        gui_conn = gui_sock.makefile('wb')
        print("Gui 1 connected")

        #User 2
        gui_sock2 = socket.socket()
        #gui_sock2.connect(('172.91.89.246',6668)) #connects to gui laptop IP of User 2
        gui_sock2.connect(('210.66.66.166',6667)) #Denny's Laptop
        print("[*] Client_user 2 listening on port")
        gui_conn2 = gui_sock2.makefile('wb')
        print("Gui 2 connected")

        while True:    
            print("running")
            image_len = struct.unpack('<L', rpi_client_conn.read(struct.calcsize('<L')))[0] #unpacks from buffer of bytes
            print(image_len)
            #image_len is a bytes like object to be written in to the image stream 
            if not image_len:
                print("no image stream was unpacked")
                break
            image_stream = io.BytesIO() #stream of bytes
            image_stream2 = io.BytesIO()
            image_stream.write(rpi_client_conn.read(image_len))  #writes the byte like object from rpi to the raw stream
            image_stream2.write(image_stream.getbuffer())
            #image_stream2.write(rpi_client_conn.read(image_len))
            #image_stream2.write(image_stream.read())
            #image_stream.truncate()
            #image_stream.seek(0)
            #image = Image.open(image_stream) #open the PIL image

            #send to multi clients
            #Send to client 1
            gui_conn.write(struct.pack('<L',image_stream.tell())) #reports the size of the entire stream at current point.. end of stream?
            gui_conn.flush() #flush content to a file...
            image_stream.seek(0)
            gui_conn2.write(struct.pack('<L',image_stream2.tell())) #reports the size of the entire stream at current point.. end of stream?
            
            gui_conn2.flush() #flush content to a file...
            image_stream2.seek(0)
            gui_conn.write(image_stream.read())
            image_stream.truncate()
            gui_conn2.write(image_stream2.read())
            #image_stream.seek(0)
            image_stream2.truncate()

        gui_conn.write(struct.pack('<L',0))
        gui_conn2.write(struct.pack('<L',0))
        
    finally:
        gui_conn.close()
        gui_sock.close()
        gui_conn2.close()
        gui_sock2.close()
        rpi_client_conn.close()
        rpi_sock.close()
    

if __name__ == "__main__":
    main()
