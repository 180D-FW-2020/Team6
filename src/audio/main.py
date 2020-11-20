"""
@author: Robert Renzo Rudio
@date: Tue Nov 17 21:42:33 2020

main: puts all audio codes together and execute.
"""

import Mic
import time

def run():
    mic = Mic.Microphone()
    mic.start()
    mic.listen()
    time.sleep(1000)
    mic.stop_listen()

if __name__ == "__main__":
    run()