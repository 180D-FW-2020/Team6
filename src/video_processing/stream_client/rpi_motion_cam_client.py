import io
import socket
import struct
import time
import picamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import imutils
import datetime

motion_reset_time = 1.0
minArea = 1000
client_socket = socket.socket()


#client_socket.connect(('192.168.1.10', 9000))  # connect to home priv ip addr Henry
client_socket.connect(('3.15.16.101',6666)) #connect to aws public ip addr.
# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    #camera.vflip = True
    camera.resolution = (640,480) #does lag increase if resolution goes up???
    # Start a preview and let the camera warm up for 2 seconds
    #camera.framerate = 30
    camera.start_preview()
    time.sleep(0)


    firstFrame = None
    firstFrame_start = time.time()


    start = time.time()
    stream = io.BytesIO()
    outstream = io.BytesIO()

    for frame in camera.capture_continuous(stream, 'jpeg',use_video_port=True): #stream is raw capture in jpeg format
        
        #Pipeline stream into another streamio object...
        stream.seek(0) #need to reset stream before reading
        file_bytes = np.asarray(bytearray(stream.read()),dtype=np.uint8) #not converting to bytes properly from bytesio
        stream.seek(0)
        stream.truncate()

        raw_frame = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)
        # if raw_frame is None:
        #    break
        text = "None Detected" 

        #motion detection
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
        tmp, buff = cv2.imencode('.jpeg',raw_frame) #returns a tuple, buff is a bytesio stream compatible object
        outstream.write(buff)
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        image_prelen = struct.pack('<L',outstream.tell())

        #print(image_prelen)
        #print(struct.unpack('<L',image_prelen))
        connection.write(struct.pack('<L', outstream.tell()))
        
        connection.flush()
        # Rewind the stream and send the image data over the wire
        outstream.seek(0)
        connection.write(outstream.read())
        # If we've been capturing for more than 30 seconds, quit
        #if time.time() - start > 60:
        #    break
        # Reset the stream for the next capture
        outstream.seek(0)
        outstream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
