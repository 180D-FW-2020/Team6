@echo off
ECHO starting sample.py
START python sample.py
ECHO starting vid_gui_client
START python ..\..\video_processing\stream_client\vid_client\vid_gui_client_latest_user1.py
ECHO starting chatclient
START python ..\..\gui\testing\chatcli.py
START python ..\..\gui\testing\sub_cmd.py
