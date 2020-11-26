#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Leondi Soetojo, Robert Renzo Rudio
@date: 12.31 AM, 16 November 2020

References:
pyaudio: https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
rms calculation: https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
"""

# Libraries
import AudioClassifier
import numpy as np
import preprocess
import pyaudio
import struct
import sys
import threading
import wave
from datetime import datetime

sys.path.append("../")
from comms import AudioServer # pylint: disable=import-error

# Load in neural network
NN_PATH = "../data/nnmv2.1.h5"
ac = AudioClassifier.AudioClassifier(NN_PATH)

# Pyaudio constants
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
swidth = 2
MAX_REC_SECONDS = 60
SAVE_PATH = "../../recordings/audio/"

audio_s = AudioServer.AudioServer()
audio_s.start()

class Microphone:
    # record_second is how long we want to record the sound
    def __init__(self, chunk=1024, channels=1, record_second=7, rate=16000, rms_thresh=20):
        self.chunk = chunk
        self.channels = channels
        self.record_second = record_second
        self.rate = rate
        self.p = None
        self.stream = None
        self.rms_thresh = rms_thresh
        self.LISTEN = True

    def start(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.chunk)

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop_listen(self):
        self.LISTEN = False

    @staticmethod
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

    def listen(self):
        thread = threading.Thread(target=self._listen)
        thread.start()

    def _listen(self):
        self.LISTEN = True
        while self.LISTEN:
            try:
                data = self.stream.read(self.chunk)
            except:
                continue
            rms = self.rms(data)
            if rms > self.rms_thresh:
                self.record()
                
    def record(self):
        print("Recording audio ...")

        sec = self.rate / self.chunk
        l = int(sec * self.record_second)
        m = int(sec * MAX_REC_SECONDS)

        frames = []
        for _ in range(0, l):
            try:
                data = self.stream.read(self.chunk)
            except:
                continue

            audio_s.send(data)
            frames.append(data)

        # Do classification on the first self.record_seconds:
        self.save_wav(frames, SAVE_PATH + "analyze.wav")
        mfcc = preprocess.audio_mfcc(SAVE_PATH + "analyze.wav", 128)
        pred = ac.predict(mfcc)
        print(pred)

        # Continue recording if noise is still deteced   
        i = sec * 2   
        while i < l:
            try:
                data = self.stream.read(self.chunk)
            except:
                continue

            audio_s.send(data)

            rms = self.rms(data)
            if rms > self.rms_thresh:
                l += sec
            
            if i > m:
                break

            i += 1
    
        audio_s.send(b"done")
        print("here")
        print("... Done recording")

    def save_wav(self, frames, fname):
        print("Saving")
        wf = wave.open(fname, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()