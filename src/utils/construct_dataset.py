#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Robert Renzo Rudio
@date: Fri Nov  6 16:44:38 2020
"""

# Imports
import argparse
import Dataset
import librosa
import sys
import numpy as np

# Reference: https://stackoverflow.com/questions/32468349/how-to-add-silence-in-front-of-a-wav-file/32477869
def pad_audio(data, sr, target):
    final_len = int(sr * target)

    # Calculate the length of padding needed.
    shape = data.shape
    pad_len = final_len - shape[0]
    shape = (pad_len,) + shape[1:]

    # Append silence data if needed.
    if shape[0] > 0:                
        if len(shape) > 1:
            return np.vstack((np.zeros(shape), data))
        else:
            return np.hstack((np.zeros(shape), data))
    else:
        return data

# Reference: https://medium.com/@mikesmales/sound-classification-using-deep-learning-8bc2aa1990b7
# Generate mfccs from an audio.
def audio_mfcc(path: str, args) -> np:
    n_mfcc = args
    audio, sr = librosa.load(path, sr=16000)
    audio = pad_audio(audio, sr, 7)
    mfccs = librosa.feature.mfcc(audio, sr=sr, n_fft=2048, hop_length=512, n_mfcc=n_mfcc)
    mfccs = mfccs[:, :219]
    return mfccs
    
# Generate raw audio.
def raw_audio(path: str) -> np:
    audio, _ = librosa.load(path)
    return audio

def main():
    usg_msg = "python3 {} -p [PATH/TO/DATA] -s [PATH/TO/SAVE/DIRECTORY]".format(sys.argv[0])
    descr = "Creates a dataset"
    parser = argparse.ArgumentParser(usage=usg_msg, description=descr)
    parser.add_argument("-p", "--path", metavar="", type=str, required=True, help="PATH to data")
    parser.add_argument("-s", "--save", metavar="", type=str, required=True, help="Filename of save")
    args = parser.parse_args()

    PATH = args.path
    SAVE = args.save

    file_extensions = ("*.wav", "*caf")
    ds = Dataset.Dataset(file_extensions=file_extensions, extract_method=audio_mfcc, args=128)
    pd = ds.create_dataset(PATH)
    print(pd)

    ds.save_dataset(pd, SAVE)

if __name__ == "__main__":
    main()