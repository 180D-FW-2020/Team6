# Test Subscribe code
# Reference: https://github.com/pholur/180D_sample

import random
from paho.mqtt import client as mqtt
import os

# The address of the subscriber to get the message from the publisher
broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
text = None

CURPATH = os.path.dirname(os.path.abspath(__file__))

def connect_mqtt() -> mqtt:
    global text
    def on_connect(client, userdata, flags, rc):
        print(f"Connection return code: {rc}")
        subscribe(client)

    def on_disconnect(client, userdata, rc):
        print(f"Disconnected with return code: {rc}") 
    
    def on_message(client, userdata, message, text=text):
        path = os.path.join(CURPATH,"notification.txt")
        f = open(path, "w+")
        new_message = message.payload.decode()
        if(text != new_message and new_message != None):
            text = new_message
        print(f"Received message: {text} on topic {message.topic} with QoS {message.qos})")
        f.write(text)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(broker, port)

    return client

def subscribe(client: mqtt):
    client.subscribe(topic)

def run():
    client = connect_mqtt()
    client.loop_forever()



if __name__ == '__main__':
    run()