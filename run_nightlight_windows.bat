@echo off
ECHO starting sample.py
START python src\gui\sample.py
ECHO starting subscription to commands (MQTT)
START python src\gui\sub_cmd.py
