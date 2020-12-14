@echo off
ECHO starting command.py

ECHO starting voice_command
START python speech_recognition\Voice_Recognition.py
CALL python commands\commands.py

ECHO some issues with commands and the database
Pause