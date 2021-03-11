@echo off
ECHO starting command.py

ECHO starting voice_command
START python speech_recognition\Voice_Recognition.py
START python commands\commands.py
ECHO starting audio
START python audio\audio.py

Pause