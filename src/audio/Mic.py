#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Leondi Soetojo, Robert Renzo Rudio
@date: 12.31 AM, 16 November 2020

References:
pyaudio: https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
rms calculation: https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
"""
import numpy as np
import pyaudio
import struct
import time
import wave

FORMAT = pyaudio.paInt16
SHORT_NORMALIZE = (1.0/32768.0)
swidth = 2
MAX_REC_SECONDS = 60 * 2

class MicRecording:
    # record_second is how long we want to record the sound
    def __init__(self, chunk=1024, channels=1, record_second=5, rate=16000, sleep=2, rms_thresh=100):
        self.chunk = chunk
        self.channels = channels
        self.record_second = record_second
        self.rate = rate
        self.p = None
        self.stream = None
        self.sleep = sleep
        self.rms_thresh = rms_thresh

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
        while True:
            data = self.stream.read(self.chunk)
            rms = self.rms(data)
            if rms > self.rms_thresh:
                self.record("to_nn.wav", True)

    def record(self, fname, for_nn):
        print("Recording audio ...")

        frames = []
        
        if for_nn:
            for _ in range(0, int(self.rate / self.chunk * self.record_second)):
                data = self.stream.read(self.chunk)
                frames.append(data)
        else:
            for _ in range(0, int(self.rate / self.chunk * MAX_REC_SECONDS)):
                data = self.stream.read(self.chunk)
                frames.append(data)
                rms = self.rms(data)
                if rms < self.rms_thresh:
                    break

        print("... Done recording")

        wf = wave.open(fname, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()