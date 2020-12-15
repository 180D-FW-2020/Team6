import pyaudio
import socket
import wave
from datetime import datetime

BUFFERSIZE = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 16000
CHUNK = 1024
sample_size = pyaudio.get_sample_size(FORMAT)
SAVE_PATH = "../../recordings/audio/"

class AudioClient:
    def __init__(self, ip="3.15.16.101", port=3001, write=False):
        self.ip = ip 
        self.port = port
        self.client_conn= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.p = None
        self.stream = None
        self.write = write
    
    def start(self):
        self.client_conn.connect((self.ip, self.port))
        print(f"Connected to {self.ip} on port {self.port}")

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=CHUNK)

    def stop(self):
        self.client_conn.shutdown(socket.SHUT_RDWR)
        self.client_conn.close()

    def recv(self):
        #frames = []
        while True:
            data = self.client_conn.recv(BUFFERSIZE)
        
            while len(data) < BUFFERSIZE:
                temp = self.client_conn.recv(BUFFERSIZE - len(data))
                data += temp
            """    
            if len(data) <= 4 and len(data) != 0:
                self.save_wav(frames)
                return
            """
            if self.write:
                self.stream.write(data)

        #frames.append(data)

    def save_wav(self, frames):
        print("Saving")
        now = datetime.now()
        now_str = now.strftime("%d-%m-%Y-%H:%M:%S.wav")

        wf = wave.open(SAVE_PATH + now_str, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_size)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

"""
def main():
    AC = AudioClient()
    AC.start()
    while True:
        AC.recv()
if __name__ == "__main__":
    main()
"""
