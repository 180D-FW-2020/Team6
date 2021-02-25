@echo off
ECHO starting sample.py
START python sample.py
ECHO starting subscription to commands (MQTT)
START python ..\..\gui\sub_cmd.py
