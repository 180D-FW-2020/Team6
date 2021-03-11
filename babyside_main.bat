@echo off
ECHO starting command.py

ECHO starting voice_command
ECHO SAY: HI NIGHTLIGHT
ECHO followed by: play first song OR play second song OR stop OR pause
START python src\speech_recognition\Voice_Recognition.py
START python src\commands\commands.py

ECHO starting audio
START python src\audio\audio.py
