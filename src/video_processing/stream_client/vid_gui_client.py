import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl

gui_client_socket = socket.socket()
gui_client_socket.connect(('3.15.16.101', 6667))  # ADD IP HERE

# Accept a single connection and make a file-like object out of it
#connection = gui_client_socket.makefile('rb')
try:
    message = "message from gui_laptop"
    byte_m = message.encode('ASCII')
    while True:
        print("sending message")
        gui_client_socket.sendall(byte_m)
        

finally:
    print("closing socket")
    gui_client_socket.close()



# try:
#     img = None
#     while True:
#         print("running")
#         # Read the length of the image as a 32-bit unsigned int. If the
#         # length is zero, quit the loop

#         connection.read(struct.calcsize('<L'))
#         print("reading")

#         image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0] #stuck here
#         print("unpacked")
#         if not image_len:
#             print("not image len")
#             break
#         # Construct a stream to hold the image data and read the image
#         # data from the connection
#         image_stream = io.BytesIO()
#         image_stream.write(connection.read(image_len))
#         # Rewind the stream, open it as an image with PIL and do some
#         # processing on it
#         image_stream.seek(0)
#         image = Image.open(image_stream)
        
#         if img is None:
#             print("Image is none")
#             img = pl.imshow(image)
            
#         else:
#             print("image is set")
#             img.set_data(image)

#         pl.pause(0.0001)
#         pl.draw()

#         #print('Image is %dx%d' % image.size)
#         #image.verify()
#         #print('Image is verified')
# finally:
#     connection.close()
#     gui_client_socket.close()