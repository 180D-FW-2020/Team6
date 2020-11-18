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
#import AudioClassifier
import numpy as np
import pyaudio
import struct
import threading
import time
import wave
from datetime import datetime

# Load in neural network
NN_PATH = "nn.h5"
#ac = AudioClassifier.AudioClassifier(NN_PATH)

# Pyaudio constants
FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
swidth = 2
MAX_REC_SECONDS = 60
SAVE_PATH = "../../recordings/audio/"

class Microphone:
    # record_second is how long we want to record the sound
    def __init__(self, chunk=1024, channels=1, record_second=7, rate=16000, rms_thresh=100):
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
        while self.LISTEN:
            data = self.stream.read(self.chunk)
            rms = self.rms(data)
            if rms > self.rms_thresh:
                nnwav_path = SAVE_PATH + "nn.wav"
                self.record(nnwav_path, True)

                # TODO: Preprocess audio saved at nnwav_path before prediction

                # Perform classification
                pred = "environment" #ac.predict(nnwav_path)
                if pred == "baby":#ac.le_mappings[0]:
                    now = datetime.now()
                    now_str = now.strftime("%d-%m-%Y-%H:%M:%S.wav")
                    self.record(SAVE_PATH + now_str, False)
        
    def record(self, fname, for_nn):
        print("Recording audio ...")

        frames = []
        
        if for_nn: # Audio to be used for classification.
            for _ in range(0, int(self.rate / self.chunk * self.record_second)):
                data = self.stream.read(self.chunk)
                frames.append(data)
        else: # Audio to be recorded won postive classification.
            sec = self.rate / self.chunk
            l = int(sec * self.record_second)
            m = int(sec * MAX_REC_SECONDS)
            i = 0
            while i < l:
                data = self.stream.read(self.chunk)
                frames.append(data)
                rms = self.rms(data)

                if rms > self.rms_thresh: 
                    # Add a second if audio is still > rms_thresh
                    l += sec
                if i > m:
                    break
                
                i += 1

        print("... Done recording")

        wf = wave.open(fname, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()