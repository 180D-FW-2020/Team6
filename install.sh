ENV_NAME=nightlight;

if [[ "$1" == "-d" ]]; then
    conda env remove -n $ENV_NAME
else
    conda create -n $ENV_NAME tensorflow
    conda activate nightlight
    conda install -n $ENV_NAME pyaudio
    conda install -n $ENV_NAME pip
    python -m pip install --upgrade pip
    pip install imutils
fi
