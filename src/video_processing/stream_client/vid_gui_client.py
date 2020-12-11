import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

#notification
import smtplib
from email.message import EmailMessage
#gui_client_socket = socket.socket()
#gui_client_socket.connect(('0.0.0.0', 6667))  # ADD IP HERE

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

motion_reset_time = 5.0 #seconds
minArea = 1000 #area of detection for motion detection trigger

gui_sock = socket.socket()
gui_sock.bind(('0.0.0.0',6667))
gui_sock.listen(0)
connection = gui_sock.accept()[0].makefile('rb')

# try:
#     while True:

#         data = gui_client_socket.recv(8192)
#         print(data)


# finally:
#     print("closing socket")
#     gui_client_socket.close()

try:
	img = None
	firstFrame = None
	firstFrame_start = time.time()
	
	while True:
		#print("running")


		image_len = struct.unpack('<L',connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			print("not image len")
			break
			#continue
		#print(image_len)
		# Construct a stream to hold the image data and read the image
		# data from the connection
		image_stream = io.BytesIO()
		#print(connection.read(image_len))
		image_stream.write(connection.read(image_len)) #stuck here
		#print("stream_written")
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
		#grab firstFrame time
		
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
			if notif_flag == False
				#for some reason this sends twice
				notify("Motion Detected from NightLight","Some movement was caught on the NightLight, check things out to make sure everything's okay :) - Your Nightlight","kouhenry@yahoo.com")
				notif_flag = True

		# draw the text and timestamp on the frame
		cv2.putText(raw_frame, "Motion Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(raw_frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

		# show the frame and record if the user presses a key
		cv2.imshow("Camera feed", raw_frame)
		cv2.imshow("Thresh", thresh)
		#cv2.imshow("Frame Delta", frameDelta)
		cv2.imshow('target area', target_area)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
		# image = Image.open(image_stream)
		# #print("image opened")

		# if img is None:
		# 	#print("Image is none")
		# 	img = pl.imshow(image)
		# else:
		# 	#print("image is set")
		# 	img.set_data(image)

		# pl.pause(0.0001)
		# pl.draw()

		# print('Image is %dx%d' % image.size)
		# image.verify()
		# print('Image is verified')
finally:
	connection.close()
	gui_client_socket.close()