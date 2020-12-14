import argparse
import paho.mqtt.client as mqtt
from playsound import playsound
import sys

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"

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
            print("soundDB/" + str_msg)
            playsound("soundDB/" + str_msg)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)
    return client

def subscribe(client: mqtt):
    client.subscribe(topic)

def main():
    client = connect_mqtt()
    client.loop_forever()
    
if __name__ == "__main__":
    main() 