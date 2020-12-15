import io
import socket
import threading
import wave
from datetime import datetime

BUFFERSIZE = 2048
SIGLEN = 6
RATE = 16000
CHUNK = 1024
CHANNELS = 1
SAMPLESIZE = 2
SEC = RATE/CHUNK
MAX_REC_SEC = 60
SAVEPATH = "recordings/audio/"

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

def main():
    audio_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_client.bind(('0.0.0.0', 2000))  # socket for RPI Microphone
    audio_client.listen(0)
    audio_conn, addr = audio_client.accept()
    print("Accepted connection from Microphone")

    gui_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    gui_client.bind(('0.0.0.0', 2001))  # socket for RPI Microphone
    gui_client.listen(0)
    gui_conn, addr = gui_client.accept()
    print("Accepted connection from GUI")

    while True:
        data = audio_conn.recv(BUFFERSIZE)        
        
        temp = None
        while len(data) != BUFFERSIZE:
            temp = audio_conn.recv(BUFFERSIZE - len(data))
            data += temp
            
        gui_conn.send(data)
        
        """
        if len(data) <= SIGLEN and len(data) != 0:
            print("HERE")
            record(audio_conn, gui_conn)
            continue
        if len(data) <= 4 and len(data) != 0:
            gui_conn.send(data)
            continue

        while len(data) < BUFFERSIZE:
            temp = audio_conn.recv(BUFFERSIZE)
            data += temp
        """

if __name__=="__main__":
    main()
