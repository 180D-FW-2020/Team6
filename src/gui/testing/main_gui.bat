@echo off
ECHO starting main_gui.py
START python sample.py
ECHO starting vid_gui_client.py
START python ..\..\video_processing\stream_client\vid_client\vid_gui_client_user1.py
ECHO starting chatclient
START python ..\..\gui\testing\chatcli.py
START python ..\..\gui\testing\sub_cmd.py
