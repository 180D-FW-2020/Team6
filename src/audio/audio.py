import atexit
import AudioClassifier
import MicClient
import os
import preprocess
import pyaudio
import signal
import struct
import sys
import wave
from datetime import datetime

# PyAudio constants.
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
p = None
stream = None

# Recording constants.
SEC = RATE / CHUNK
MAX_REC_SECONDS = 7

# RMS constants.
SWIDTH = 2
SHORT_NORMALIZE = (1.0/32768.0)
RMS_THRESH=20

# Audio classifier.
print("Loading Neural Network...")
NN = "nnmv2.1.h5"
AC = AudioClassifier.AudioClassifier(NN)
print("... Done")

# TCP connection.
conn = MicClient.MicClient()
conn.start()

# Controls
if os.name == 'nt':
    SAVEPATH = "AudioDb\\"
else:
    SAVEPATH = "AudioDb/"
RECORD = False

def save_wav(frames, fname):
    global p
    print("Saving...")
    wf = wave.open(fname, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("...Saved")

def rms(frame):
    count = len(frame) / SWIDTH
    format = "%dh" % (count)
    shorts = struct.unpack(format, frame)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * SHORT_NORMALIZE
        sum_squares += n * n
    rms = (sum_squares / count) ** 0.5
    return rms * 1000

def start_mic():
    global p, stream
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

def stop_mic():
    global p, stream
    stream.stop_stream()
    stream.close()
    p.terminate()

def record():
    global stream, RECORD
    print("Recording audio ...")

    frames = []

    # Record for neural net.
    num_chunk = int(SEC * 7)
    for i in range(num_chunk):
        try:
            data = stream.read(CHUNK)
            conn.send(data)
            frames.append(data)
        except:
            continue
                
    print(SAVEPATH + "nn.wav")
    save_wav(frames, SAVEPATH + "nn.wav")
    mfcc = preprocess.audio_mfcc(SAVEPATH + "nn.wav", 128)
    AC.predict(mfcc)
            
    # Record for about MAX_REC_SECONDS.
    num_chunk = int(SEC * MAX_REC_SECONDS)
    for _ in range(num_chunk):
        try:
            data = stream.read(CHUNK)
            conn.send(data)
            frames.append(data)
        except:
            continue
    
    if RECORD:
        now = datetime.now()
        now_str = now.strftime("%d-%m-%Y-%H:%M:%S.wav")
        save_wav(frames, now_str)

    print("... Done recording")

def listen():
    global stream
    while True:
        try:
            data = stream.read(CHUNK)
            conn.send(data)
            _rms = rms(data)
        except:
            continue
        
        if _rms > RMS_THRESH:
            record()

def main():
    start_mic()
    listen()
    stop_mic()

if __name__ == "__main__":
    atexit.register(stop_mic)
    main()
