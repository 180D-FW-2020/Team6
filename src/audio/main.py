import Mic
import threading
import time

def run():
    mic = Mic.Microphone()
    mic.start()
    mic.listen()
    time.sleep(10)
    mic.stop_listen()

if __name__ == "__main__":
    run()