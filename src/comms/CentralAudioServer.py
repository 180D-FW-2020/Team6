#!/usr/bin/env python

import io
import socket
import threading
import wave
from datetime import datetime

SIGLEN = 6
RATE = 16000
CHUNK = 1024
BUFFERSIZE = CHUNK
CHANNELS = 1
SAMPLESIZE = 2
SEC = RATE/CHUNK
MAX_REC_SEC = 60
SAVEPATH = "recordings/audio/"

mutex = threading.Lock()

AUDIO = None
CLIENTS = []

def redirect():
    global AUDIO, CLIENTS

    while not AUDIO:
        pass
    
    while True:
        closed = []

        # Read from RPi (AUDIO)
        data = AUDIO.recv(BUFFERSIZE)
    
        # Redirect data from AUDIO to CLIENTS
        mutex.acquire()
        for client in CLIENTS:
            try:
                client.send(data)
            except:
                closed.append(client)

        # Dropping closed connections       
        for drop in closed:
            CLIENTS.remove(drop)

        mutex.release()

def client_connection():
    global CLIENTS
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('0.0.0.0', 4000))  # socket for listening
    listen_sock.listen(5)

    while True:
        cli, _ = listen_sock.accept()
        mutex.acquire()
        CLIENTS.append(cli)
        mutex.release()

        print("Accepted connection from client")

def audio_connection():
    global AUDIO 
    
    audio_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_client.bind(('0.0.0.0', 4001))  # socket for RPI Microphone
    audio_client.listen(0)
    AUDIO, _ = audio_client.accept()
    print("Accepted connection fro RPI Microphone")

def main():
    client_listner_thread = threading.Thread(target=client_connection)
    client_listner_thread.start()

    audio_listner_thread = threading.Thread(target=audio_connection)
    audio_listner_thread.start()

    redirect_thread = threading.Thread(target=redirect)
    redirect_thread.start()
        
if __name__== "__main__":
    print("Audio Server Is Running")
    main()