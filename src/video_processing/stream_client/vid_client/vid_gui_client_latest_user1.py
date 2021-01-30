import io
import socket
import struct
#from PIL import Image
#import matplotlib.pyplot as pl
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

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

motion_reset_time = 5.0 #seconds
minArea = 1000 #area of detection for motion detection trigger

motion_detect = False

# gui_sock = socket.socket()
# gui_sock.bind(('0.0.0.0',6667))
# gui_sock.listen(0)
# connection = gui_sock.accept()[0].makefile('rb')
gui_sock = socket.socket()
gui_sock.connect(('3.140.200.49',6667)) # connect to AWS Server's public IP
print("Client User listening on port...")
connection = gui_sock.makefile('rb')
print("Client User 1 connected")

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
		print(image_len)
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
		cv2.imshow("Camera feed", raw_frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key is pressed, break from the lop
		if key == ord("q"): #note imshow doesn't work without waitkey
			connection.close()
			gui_sock.close()
			break
except:
	print("Occurred Exception, closing socket")
	connection.close()
	gui_sock.close()

finally:
	connection.close()
	gui_sock.close()
