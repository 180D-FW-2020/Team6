import json
import os
import paho.mqtt.client as mqtt
from playsound import playsound
import sys
import threading
import os
from audioplayer import AudioPlayer

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/team6/lullaby"

ap = None

# PATHS
SRCPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DBPATH = os.path.join(SRCPATH, 'database')
EMAILPATH = os.path.join(SRCPATH, 'notification', 'emails.txt')
SOUNDDBPATH = os.path.join(SRCPATH, 'commands', 'soundDB')
sys.path.append(DBPATH)

# Database object
from DBInterface import DBInterface #pylint: disable=import-error

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        print(f"Connection return code: {rc}")
        subscribe(client)

    def on_disconnect(client, userdata, rc):
        print(f"Disconnected with return code: {rc}") 
    
    def on_message(client, userdata, message):
        str_msg = message.payload.decode()
        if "lullaby" in str_msg:
            print(f"Received command: {str_msg}")
            soundpath = os.path.join(SOUNDDBPATH, str_msg)
            play_sound(soundpath)

        if "pause" in str_msg:
            print(f"Received pause: {str_msg}")
            pause_sound()

        if "resume" in str_msg:
            print(f"Recieved resume: {str_msg}")
            resume_sound()
        
        if "update email" == str_msg:
            print("Received update email list.")
            get_email()
 
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)
    return client

def play_sound(PATH):
    global ap

    if ap is not None:
        stop_sound()

    ap = AudioPlayer(PATH)
    ap.play(block=False) 

def stop_sound():
    ap.stop()
    ap.close()

def pause_sound():
    ap.pause()

def resume_sound():
    ap.resume()

def subscribe(client: mqtt):
    client.subscribe(topic)

def get_email():
    try:
        db = DBInterface()
        emails = json.loads(db.get_email(option=1))['emails']
        emails = (','.join(emails))

        with open(EMAILPATH, "w") as f:
            print("Email list updated.")
            f.write(emails)
        f.close()

    except:
        print("Unable to FETCH emails from database server.")

def main():
    if not os.path.exists(EMAILPATH):
        with open(EMAILPATH, "w") as f:
            pass
        f.close()

    get_email()
    client = connect_mqtt()
    client.loop_forever()
    
if __name__ == "__main__":
    main()
