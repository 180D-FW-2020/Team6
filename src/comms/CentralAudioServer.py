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

AUDIO = None

def redirect(CLIENT):
    global AUDIO

    while not AUDIO:
        pass
    
    while True:
        data = AUDIO.recv(BUFFERSIZE)
        CLIENT.send(data)


def client_connection(): 
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(('0.0.0.0', 4000))  # socket for listening
    listen_sock.listen(5)

    while True:
        cli, addr = listen_sock.accept()
        redirect_thread = threading.Thread(target=redirect, args=(cli,))
        redirect_thread.start()
        print("Accepted connection from client")

def audio_connection():
    global AUDIO 
    
    audio_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_client.bind(('0.0.0.0', 4001))  # socket for RPI Microphone
    audio_client.listen(0)
    AUDIO, addr = audio_client.accept()
    print("Accepted connection fro RPI Microphone")

def main():
    client_listner_thread = threading.Thread(target=client_connection)
    client_listner_thread.start()

    audio_listner_thread = threading.Thread(target=audio_connection)
    audio_listner_thread.start()
        
if __name__== "__main__":
    print("Audio Server Is Running")
    main()

"""
def rms(frame):
    count = len(frame) / swidth
    format = "%dh" % (count)
    shorts = struct.unpack(format, frame)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
    rms = (sum_squares / count) ** 0.5
    return rms * 1000

def save_wav(frames):
    print("Saving...")
    now = datetime.now()
    now_str = now.strftime("%d-%m-%Y-%H:%M:%S.wav")

    wf = wave.open(SAVEPATH + now_str, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(SAMPLESIZE)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("...Saved")

def record(audio_conn, gui_conn):

    print("Recording Audio ...")

    max_iter = int(SEC * MAX_REC_SEC)
    frames = []
    temp = None
    for i in range(max_iter):
        data = audio_conn.recv(BUFFERSIZE)
        datalen = len(data)

        while datalen != 2048:
            temp = audio_conn.recv(BUFFERSIZE-datalen) 
            data += temp

        gui_conn.send(data)
        frames.append(data)

    print("...Done Recording")

    th = threading.Thread(target=save_wav, args=(frames,))
    th.start()
"""
