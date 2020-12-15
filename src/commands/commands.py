import paho.mqtt.client as mqtt
import threading
from playsound import playsound
from audioplayer import AudioPlayer
import sys

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/team6/lullaby"

ap = None

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
            play_sound("soundDB/" + str_msg)

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

def main():
    client = connect_mqtt()
    client.loop_forever()
    
if __name__ == "__main__":
    main()
