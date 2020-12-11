import argparse
import paho.mqtt.client as mqtt
import random
import sys
import time

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/team6/lullaby"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt() -> mqtt:
    def on_connect(client, userdata, flags, rc):
        print(f"Connection returned code: {rc}")

    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client

def publish(client: mqtt, msg):
    status, _ = client.publish(topic, msg)

    if status == 0:
        print(f"Sending: {msg}")
    else:
        print("Error in sending a message")