# Author = Leondi Soetojo
# Submit Time = 12.31 AM, 16 November 2020

import pyaudio
import wave

FORMAT = pyaudio.paInt16
FILENAME = "Recording_Sound.wav"


# Refrence: https://stackoverflow.com/questions/35344649/reading-input-sound-signal-using-python
#def recording_Mic():
class MicRecording:
    # record_second is how long we want to record the sound
    def __init__(self, chunk, channel, record_second, rate):
        self.chunk = chunk
        self.channel = channel
        self.record_second = record_second
        self.rate = rate


    def record(self):

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=self.channel,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)

        print("* recording")

        frames = []

        for i in range(0, int(self.rate / self.chunk * self.record_second)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(FILENAME, 'wb')
        wf.setnchannels(self.channel)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

p1 = MicRecording(1024, 2, 5, 44100)
p1.record()
