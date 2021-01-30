#!usr/bin/env python
import io
from PIL import Image
import struct
import matplotlib.pyplot as pl
import socket
import sys
import threading
import numpy as np
import cv2
import time
import datetime
import imutils

#notification
import smtplib
from email.message import EmailMessage

_email = "nightlight.notifier@gmail.com" # sender email addr
_pass =  "qjhlwonnufdgvdss" # sender email password

def notify(subject, content, to):
    print("Pushing notification")
    msg = EmailMessage()
    msg.set_content(content)
    msg["subject"] = subject
    msg["from"] = _email
    msg["to"] = to 
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(_email, _pass)
    server.send_message(msg)
    server.quit()

motion_reset_time = 1.0 #seconds
minArea = 1000 #area of detection for motion detection trigger

CLIENTS = []
RPI_CLIENT_CONN = None

mutex = threading.Lock()
motion_detect = True
notif_flag = False

processed_stream = io.BytesIO() #hold output after motion processing

def rpi_connect():
    global RPI_CLIENT_CONN
    host = '0.0.0.0'
    port = 6666
    tot_socket = 2
    rpi_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rpi_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    rpi_sock.bind((host, port))
    rpi_sock.listen(10)
    print("[*] Server listening on port for RPI")
    RPI_CLIENT_CONN = rpi_sock.accept()[0].makefile('rb')
    print("Rpi connected")

def client_connect():#thread function for client_listener_thread
    global CLIENTS
    gui_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    gui_sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    gui_sock.bind(('0.0.0.0', 6662)) #potential issue with multiple clients?
    gui_sock.listen(10)
    
    while True:
        print("[*] Server listening on port for Video Client")
        gui_conn = gui_sock.accept()[0].makefile('wrb')
        mutex.acquire()
        CLIENTS.append(gui_conn)
        mutex.release()
        print("GUI client connected")

def send_data(): #thread function for send_data_thread
    global RPI_CLIENT_CONN, CLIENTS

    while not RPI_CLIENT_CONN:
        pass

    img = None
    firstFrame = None
    firstFrame_start = time.time()
    
    while True:
        closed = []
        image_len = struct.unpack('<L', RPI_CLIENT_CONN.read(struct.calcsize('<L')))[0] #unpacks from buffer of bytes
        print(image_len) #image_len is a bytes like object to be written in to the image stream 
        
        if not image_len:
            print("no image stream was unpacked")
            break
        image_stream = io.BytesIO() #create stream object
        image_stream.write(RPI_CLIENT_CONN.read(image_len))



        #motion detection
        if motion_detect is True:
            img = None
            firstFrame = None
            firstFrame_start = time.time()
            file_bytes = np.asarray(bytearray(image_stream.read()),dtype=np.uint8) #not converting to bytes properly from bytesio
            image_stream.seek(0)
            image_stream.truncate()

            raw_frame = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
            # if raw_frame is None:
            #    break
            text = "None Detected" 

            #cv2.imshow("Camera feed", raw_frame)
            #drawing crib...
            height, width = raw_frame.shape[0], raw_frame.shape[1]
            target_upper_left = (((width//2)-200),((height//2)-200)) #setting up coords for target area
            target_lower_right = (((width//2)+200),((height//2)+200))
            target_box = cv2.rectangle(raw_frame,target_upper_left,target_lower_right,(255,0,0),3) #stream works till here
            target_area = raw_frame[target_upper_left[1]:target_lower_right[1], target_upper_left[0]:target_lower_right[0]] #y1:y2,x1:x2 where y is lower_right, and x is upper left

            # resize the target area, convert it to grayscale, and blur it
            frame = imutils.resize(target_area, width=500, inter=cv2.INTER_NEAREST)
            gray = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            # grab firstFrame time
            
            firstFrame_end = time.time()
            if firstFrame_end - firstFrame_start > motion_reset_time:
                firstFrame_start = firstFrame_end
                #print("resetting image")
                firstFrame  = None
            if firstFrame is None:
                firstFrame = gray
                continue

            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            thresh = thresh.astype(np.uint8)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # loop over the contours
            notif_flag = False
            for c in cnts:

                # if the contour is too small, ignore it
                if cv2.contourArea(c) < minArea:
                    continue
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Detected!"
                if notif_flag is False:
                #for some reason this sends twice
                    #notify("Motion Detected from NightLight","Some movement was caught on the NightLight, check things out to make sure everything's okay :) - Your Nightlight","8312334058@txt.att.net")
                    notif_flag = True

            # draw the text and timestamp on the frame
            cv2.putText(raw_frame, "Motion Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.putText(raw_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

            #Streaming feed
            tmp, processed_stream = cv2.imencode('.jpeg',raw_frame) #returns a tuple, buff is a bytesio stream compatible object

        else: #motion detection is false
            #processed_stream = io.BytesIO() #is this editing the global version
            processed_stream.write(image_stream.getbuffer())
            
        mutex.acquire()
        for client_conn in CLIENTS: #each client is a socket connection
            try:
                image_stream_client = io.BytesIO() #each client has their own stream
                image_stream_client.write(processed_stream.getbuffer())

                client_conn.write(struct.pack('<L',image_stream_client.tell()))
                client_conn.flush()
                image_stream_client.seek(0)

                client_conn.write(image_stream_client.read())
                image_stream_client.truncate()

            except:
                #client_conn.close() #ISSUE, need better exception handling to continue once client is cut
                print("Exception occurred wih video client: " + str(client_conn))
                closed.append(client_conn)
                #client_conn.close()

        for drop in closed:
            CLIENTS.remove(drop)
            #drop.close()

        mutex.release()

    mutex.acquire()
    for client_conn in CLIENTS:
        try:
            client_conn.write(struct.pack('<L',0))
        except:
            client_conn.close()
    mutex.release()


def main():
    #threads perform services on clients

    #RPI thread has RPI client data
    rpi_listener_thread = threading.Thread(target=rpi_connect)
    rpi_listener_thread.start()

    #thread listens for video clients and connects them to a stream
    client_listener_thread = threading.Thread(target=client_connect)
    client_listener_thread.start()

    #thread sends data to clients
    send_data_thread = threading.Thread(target=send_data)
    send_data_thread.start()

if __name__ == "__main__":
    main()
