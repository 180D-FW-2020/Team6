import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import pickle
import zlib

server_socket_rpi = socket.socket()
server_socket_laptop = socket.socket()
#server_socket.bind(('192.168.1.239', 8000))  #Local IP
server_socket_rpi.bind(('0.0.0.0',8000)) #public IP port from RPI client
server_socket_laptop.bind(('0.0.0.0',8001)) #public IP port to Laptop client
server_socket_rpi.listen(0)
server_socket_laptop.listen(0)

# Accept a single connection and make a file-like object out of it
connection_rpi = server_socket_rpi.accept()[0].makefile('rb')
connection_laptop = server_socket_laptop.accept()[0].makefile('wb')

try:
    img = None
    firstFrame = None
    minArea = 1000

    #crib detection would go here
    #grab the first frame, convert into opencv type
    #look for rectangular outline of a particular size. if found, mark outline on camera
    #go into motion detection sequence 

    while True:
    	print("Running")
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection_rpi.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection_rpi.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        
        #motion detection
        file_bytes = np.asarray(bytearray(image_stream.read()),dtype=np.uint8)
        raw_frame = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
        if raw_frame is None:
                break
        text = "None Detected"
        


        #drawing crib...
        height, width = raw_frame.shape[0], raw_frame.shape[1]
        target_upper_left = (((width//2)-200),((height//2)-200)) #setting up coords for target area
        target_lower_right = (((width//2)+200),((height//2)+200))
        target_box = cv2.rectangle(raw_frame,target_upper_left,target_lower_right,(255,0,0),3)
        target_area = raw_frame[target_upper_left[1]:target_lower_right[1], target_upper_left[0]:target_lower_right[0]] #y1:y2,x1:x2 where y is lower_right, and x is upper left

        # resize the target area, convert it to grayscale, and blur it
        frame = imutils.resize(target_area, width=500)
        gray = cv2.cvtColor(np.float32(frame), cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
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
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < minArea:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Detected!"

        # draw the text and timestamp on the frame
        cv2.putText(raw_frame, "Motion Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(raw_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
        #cv2.imshow("Camera feed", raw_frame)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)
        #cv2.imshow('target area', target_area)

        #send the finished feed to laptop client, raw_frame
        data = pickle.dumps(raw_frame,0)
        size = len(data)
        server_socket_laptop.sendall(struct.pack(">L",size)+data) #not sure what >L means
        
        key = cv2.waitKey(1) & 0xFF

finally:
	print("Closing")
    connection_rpi.close()
    connection_laptop.close()
    server_socket_rpi.close()
    server_socket_laptop.close()