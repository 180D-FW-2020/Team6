import atexit
import AudioClassifier
import MicClient
import os
import preprocess
import pyaudio
import struct
import sys
import threading
import wave
from datetime import datetime
from pathlib import Path

# PyAudio constants.
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
p = None
stream = None

# Recording constants.
SEC = RATE / CHUNK
MAX_REC_SECONDS = 20

# RMS constants.
SWIDTH = 2
SHORT_NORMALIZE = (1.0/32768.0)
RMS_THRESH=20

# Paths
CURPATH = os.path.dirname(os.path.abspath(__file__))
PARPATH = os.path.dirname(CURPATH)
BASEPATH = os.path.dirname(PARPATH)
SAVEPATH = os.path.join(CURPATH, "AudioDB")
BASERELPATH = os.path.join(os.path.basename(BASEPATH), 
                           os.path.relpath(SAVEPATH, BASEPATH))

# Audio classifier.
print("Loading Neural Network...")
NNPATH = os.path.join(CURPATH, "nnmv2.1.h5")
print(NNPATH)
AC = AudioClassifier.AudioClassifier(NNPATH)
print("... Done")

# s3 interface
S3PATH = os.path.join(PARPATH, "s3")
sys.path.append(S3PATH)
import s3Client
s3i = s3Client.S3Interface()

# TCP connection.
conn = MicClient.MicClient()
conn.start()

# Controls
RECORD = False
#RECORD = True

def upload(name, pathname):
    try:
        res = s3i.post_one(name=name, pathname=pathname)
        os.remove(pathname)
    except:
        res = s3i.post_one(name=name, pathname="temp.wav")
        os.remove("temp.wav")    

def save_wav(frames, fname):
    global p
    try:
        wf = wave.open(fname, 'wb')
    except:
        wf = wave.open("temp.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

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
    print("┬── Recording for Neural Net ...", end="\r")

    frames = []

    # Record for neural net.
    num_chunk = int(SEC * 7)
    for _ in range(num_chunk):
        try:
            data = stream.read(CHUNK)
            conn.send(data)
            frames.append(data)
        except:
            continue
    
    print("┬── Recording for Neural Net ... Done")
    savepath = os.path.join(SAVEPATH, "nn.wav")
    save_wav(frames, savepath)
    mfcc = preprocess.audio_mfcc(savepath, 128)
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
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        fname = now_str + ".wav"
        savepath = os.path.join(SAVEPATH, fname)

        save_wav(frames, savepath)

        thread = threading.Thread(target=upload, args=(fname,savepath))
        thread.start()
    
    print("└── Recording for Storage ... Done")
        

def listen():
    global stream
    print("\n** Noise Dectection Mode **")
    while True:
        try:
            data = stream.read(CHUNK)
            conn.send(data)
            _rms = rms(data)
        except:
            continue
        
        if _rms > RMS_THRESH:
            print("!!! Noise Detected !!!\n\n ** Recording Mode **")
            record()
            print("\n** Noise Dectection Mode **")

def main():
    try:
        start_mic()
        listen()
        stop_mic()
    finally:
        conn.stop()

if __name__ == "__main__":
    atexit.register(stop_mic)
    main()
