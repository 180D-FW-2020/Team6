#!usr/bin/env python
import io
from PIL import Image
import struct
import matplotlib.pyplot as pl
import socket
import sys
import threading

CLIENTS = []
RPI_CLIENT_CONN = None

mutex = threading.Lock()

def rpi_connect():
    global RPI_CLIENT_CONN
    host = '0.0.0.0'
    port = 6666
    tot_socket = 2
    rpi_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rpi_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    rpi_sock.bind((host, port))
    rpi_sock.listen(10)
    print("[*] Server listening on port for RPI")
    RPI_CLIENT_CONN = rpi_sock.accept()[0].makefile('rb')
    print("Rpi connected")

def client_connect():#thread function for client_listener_thread
    global CLIENTS
    gui_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    gui_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    gui_sock.bind(('0.0.0.0', 6667))
    gui_sock.listen(10)
    
    while True:
        print("[*] Server listening on port for Video Client")
        gui_conn = gui_sock.accept()[0].makefile('wrb')
        mutex.acquire()
        CLIENTS.append(gui_conn)
        mutex.release()
        print("GUI client connected")

def send_data(): #thread function for send_data_thread
    global RPI_CLIENT_CONN, CLIENTS

    while not RPI_CLIENT_CONN:
        pass

    while True:
        closed = []
        image_len = struct.unpack('<L', RPI_CLIENT_CONN.read(struct.calcsize('<L')))[0] #unpacks from buffer of bytes
        print(image_len) #image_len is a bytes like object to be written in to the image stream 
        
        if not image_len:
            print("no image stream was unpacked")
            break
        image_stream = io.BytesIO() #create stream object
        image_stream.write(RPI_CLIENT_CONN.read(image_len))

        mutex.acquire()
        for client_conn in CLIENTS: #each client is a socket connection
            try:
                image_stream_client = io.BytesIO() #each client has their own stream
                image_stream_client.write(image_stream.getbuffer())

                client_conn.write(struct.pack('<L',image_stream_client.tell()))
                client_conn.flush()
                image_stream_client.seek(0)

                client_conn.write(image_stream_client.read())
                image_stream_client.truncate()

            except:
                #client_conn.close()
                print("Exception occurred wih video client: " + str(client_conn))
                closed.append(client_conn)
                client_conn.close()

        for drop in closed:
            CLIENTS.remove(drop)
            drop.close()

        mutex.release()

    mutex.acquire()
    for client_conn in CLIENTS:
        try:
            client_conn.write(struct.pack('<L',0))
        except:
            client_conn.close()
    mutex.release()


def main():
    #threads perform services on clients

    #RPI thread has RPI client data
    rpi_listener_thread = threading.Thread(target=rpi_connect)
    rpi_listener_thread.start()

    #thread listens for video clients and connects them to a stream
    client_listener_thread = threading.Thread(target=client_connect)
    client_listener_thread.start()

    #thread sends data to clients
    send_data_thread = threading.Thread(target=send_data)
    send_data_thread.start()

if __name__ == "__main__":
    main()
