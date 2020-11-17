#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 08:21:16 2020

@author: DennyTsai
"""

import IPython.display as ipd
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
import numpy as np

#ipd.Audio('/Users/DennyTsai/Desktop/Audio-Signal-Processing/Baby.wav')
filename = '/Users/DennyTsai/Desktop/Audio-Signal-Processing/Baby.wav'
plt.figure(figsize=(12,4))
data,sample_rate = librosa.load(filename)
_ = librosa.display.waveplot(data,sr=sample_rate)
ipd.Audio(filename)


librosa_audio, librosa_sample_rate = librosa.load(filename) 
scipy_sample_rate, scipy_audio = wav.read(filename) 

print('Original sample rate:', scipy_sample_rate) 
print('Librosa sample rate:', librosa_sample_rate)

print('Original audio file min~max range:', np.min(scipy_audio), 'to', np.max(scipy_audio))
print('Librosa audio file min~max range:', np.min(librosa_audio), 'to', np.max(librosa_audio))

plt.figure(figsize=(12, 4))
plt.plot(scipy_audio)

plt.figure(figsize=(12, 4))
plt.plot(librosa_audio)


mfccs = librosa.feature.mfcc(y=librosa_audio, sr=librosa_sample_rate, n_mfcc=45)
print(mfccs.shape)

librosa.display.specshow(mfccs, sr=librosa_sample_rate, x_axis='time')