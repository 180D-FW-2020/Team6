@echo off
ECHO starting GUI.py
START python src\gui\GUI.py
ECHO starting subscription to commands (MQTT)
START python src\gui\sub_cmd.py
