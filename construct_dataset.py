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

# Generate mfccs from an audio.
# https://medium.com/@mikesmales/sound-classification-using-deep-learning-8bc2aa1990b7
def audio_mfcc(path: str, args) -> np:
    n_mfcc = args
    audio, sr = librosa.load(path)
    mfcc = librosa.feature.mfcc(audio, sr=sr, n_mfcc=n_mfcc)
    mfcc_scaled = np.mean(mfcc.T, axis=0)

    return mfcc_scaled
    
# Generate raw audio.
def raw_audio(path: str) -> np:
    audio, _ = librosa.load(path)
    return audio

def main():
    usg_msg = "python3 {} -p [PATH/TO/DATA] -s [PATH/TO/SAVE/DIRECTORY]".format(sys.argv[0])
    descr = "Creates a dataset"
    parser = argparse.ArgumentParser(usage=usg_msg, description=descr)
    parser.add_argument("-p", type=str, required=True, help="PATH to dataset")
    parser.add_argument("-s", type=str, required=False, help="Save the dataset into a pickle file.")
    args = parser.parse_args()

    PATH = args.p
    SAVE = args.s

    ds = Dataset.Dataset(file_extension="*.wav", extract_method=audio_mfcc, args=40)
    pd = ds.create_dataset(PATH)
    print(pd)

    if SAVE:
        ds.save_dataset(pd, SAVE)

if __name__ == "__main__":
    main()