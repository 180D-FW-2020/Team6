# Test Subscribe code
# Reference: https://github.com/pholur/180D_sample

import random
from paho.mqtt import client as mqtt_client

# The address of the subscriber to get the message from the publisher
broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
message = None


def connect_mqtt() -> mqtt_client:
# 0. define callbacks - functions that run when events happen.
# The callback for when the client receives a CONNACK response from the server.
# Not 0, the callback of the client when it disconnects.
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    
    # Add callbacks to client.
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
# The default message callback.
# (you can create separate callbacks per subscribed topic)
    def on_message(client, userdata, msg):
        global message 
        message = msg.payload.decode()
        print(f"Received `{message}` from `{msg.topic}` topic")


    client.subscribe(topic)
    client.on_message = on_message

def get_mes():
    return message


def run():
    client = connect_mqtt()
    subscribe(client)
    print (get_mes())
    client.loop_forever()


if __name__ == '__main__':
    run()

