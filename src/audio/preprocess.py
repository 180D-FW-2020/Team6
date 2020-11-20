import librosa
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