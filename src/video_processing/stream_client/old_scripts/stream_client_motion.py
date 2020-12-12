import io
import socket
import struct
import time
import picamera
import picamera.array
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

client_socket = socket.socket()

client_socket.connect(('192.168.1.10', 80))  # ADD IP HERE
#client_socket.connect(('172.91.89.246',80))
# Make a file-like object out of the connection
connection = client_socket.makefile('wb')

try:
	with picamera.PiCamera() as camera:
    camera.start_preview()
    time.sleep(2)
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        image = stream.array



    
    for foo in camera.capture_continuous(stream, 'jpeg'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        # If we've been capturing for more than 30 seconds, quit
        #if time.time() - start > 60:
        #    break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
