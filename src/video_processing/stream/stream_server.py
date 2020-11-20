import socket
import subprocess
import os

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('192.168.1.239', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    #cmdline = ['vlc', '--demux', 'h264', '-']
    #cmdline = ["C:/", "Program Files(x86)", "VideoLAN", "VLC", "vlc.exe"]
    #cmdline = ['mplayer', '-fps', '25', '-cache', '1024', '-']
    player = subprocess.Popen("C:/Program Files/VideoLAN/VLC/vlc.exe", stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        print("data_read")
        if not data:
            print("no data")
            break
        player.stdin.write(data)
finally:
    connection.close()
    server_socket.close()
    player.terminate()