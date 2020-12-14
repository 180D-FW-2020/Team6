# Test Subscribe code
# Reference: https://github.com/pholur/180D_sample

import random
from paho.mqtt import client as mqtt_client


class sub_cmd:
    def __init__(self, port, topic):
        # The address of the subscriber to get the message from the publisher
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topic = "/python/mqtt/"
        # generate client ID with pub prefix randomly
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'


    def connect_mqtt(self) -> mqtt_client:
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
        self.client = mqtt_client.Client(self.client_id)
        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        return client


    def subscribe(self, client: mqtt_client):
    # The default message callback.
    # (you can create separate callbacks per subscribed topic)
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe(self.topic)
        self.client.on_message = on_message


    def run(self):
        self.client = self.connect_mqtt()
        self.subscribe(self.client)
        self.client.loop_forever()


if __name__ == '__main__':
    s = sub_cmd()
    s.run()

