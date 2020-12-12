import io
import socket
import struct
from PIL import Image
import matplotlib.pyplot as pl

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))  #server socket for receiving from RPI and CAMERA
server_socket.listen(0)
connection = server_socket.accept()[0].makefile('rb')


gui_socket = socket.socket()
gui_socket.bind(('0.0.0.0',8002)) #server socket for transmitting to GUI
gui_socket.listen(8)

#gui_socket.listen(5)

#while True:
#    print("waiting for connection from gui client")
#    connection_gui,client_address = gui_socket.accept()
#    from_client = ''
#try:
#    print("connected to " + client_address)
#    while True:
#        data = "string from server"
#        connection_gui.sendall(data)
#finally:
#    connection_gui.close()




# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
connection_gui = gui_socket.accept()[8].makefile('wb') #TODO WB?RB?
try:
    img = None
    while True:
        print("running")
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
        
        # if img is None:
        #     img = pl.imshow(image)
        # else:
        #     img.set_data(image)

        # pl.pause(0.0001)
        # pl.draw()

        #Sending to gui client
        connection_gui.write(struct.pack('<L', image.tell()))
        print("sent to gui")
        image.seek(0)
        #image.truncate()


        #print('Image is %dx%d' % image.size)
        #image.verify()
        #    break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        #image_stream = io.BytesIO()
        #image_
        #print('Image is verified')
finally:
    connection_gui.write(struct.pack('<L', 0))
    print("closing")
    connection_gui.close()
    connection.close()
    server_socket.close()
    gui_socket.close()
