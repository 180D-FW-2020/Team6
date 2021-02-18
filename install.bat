echo Nightlight install Script for Windows ...
echo Installing nightlight environment in Anaconda ...
echo This script is untested

call conda create -n nightlight tensorflow
call conda activate nightlight
call conda install -n nightlight pyaudio
call conda install -n nightlight pip
call pip install imutils

pause
exit
