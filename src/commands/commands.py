import os
import paho.mqtt.client as mqtt
from playsound import playsound
import sqlite3
import sys
import threading
from audioplayer import AudioPlayer

broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt/team6/lullaby"

ap = None

# sqlite3
CURPATH = os.path.dirname(os.path.abspath(__file__))
PARPATH = os.path.dirname(CURPATH)
DBPATH = os.path.join(PARPATH, "sql", "RPi.db")

db = sqlite3.connect(DBPATH)
cursor = db.cursor()

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

        if "pause" in str_msg:
            print(f"Received pause: {str_msg}")
            pause_sound()

        if "resume" in str_msg:
            print(f"Recieved resume: {str_msg}")
            resume_sound()
 
        if "insert" in str_msg:
            print(f"Received command: insert")
            info = str_msg[7:].split(" ")
            name = info[0]
            email = info[1]
            query = "INSERT INTO user(name, email) VALUES(?, ?)"
            try:
                cursor.execute(query, (name, email))
                print(f"inserted username: {name} email: {email} into the database")
            except:
                print("Discarding query, duplicate found.")
                pass # Query error or duplicate entry

            db.commit()
        
        if "change" in str_msg:
            print(f"Received command: change")
            info = str_msg[7:].split(" ")
            curr = info[0]
            new = info[1]
            query = "UPDATE user SET email=? WHERE email=?"

            try:
                cursor.execute(query, (new, curr))
                print(f"Updated email from {curr} into {new}")
            except:
                print("Update failed")

            db.commit()
        
        if "alert" in str_msg:
            print(f"Received command: alert")
            info = str_msg[6:].split(" ")
            email = info[0]
            settings = info[1]
            query = "UPDATE user SET alert=? WHERE email=?"
            
            try:
                cursor.execute(query, (settings, email))
                print(f"Updated notification setting for {email} to {settings}")
            except:
                print("Updated failed")

            db.commit()
            
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
