@echo off
ECHO starting GUI.py
START python src\gui\repacked_gui.py
ECHO starting subscription to commands (MQTT)
START python src\gui\sub_cmd.py
