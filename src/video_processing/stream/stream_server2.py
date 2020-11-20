import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl

server_socket = socket.socket()
#server_socket.bind(('192.168.1.239', 8000))  # ADD IP HERE
server_socket.bind(('172.91.89.246',8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    img = None
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        image = Image.open(image_stream)
        
        if img is None:
            img = pl.imshow(image)
        else:
            img.set_data(image)

        pl.pause(0.0001)
        pl.draw()

        #print('Image is %dx%d' % image.size)
        #image.verify()
        #print('Image is verified')
finally:
    connection.close()
    server_socket.close()