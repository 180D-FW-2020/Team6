# Project NightLight
## Team 6: Henry Kou, Leondi Soetojo, Robert Renzo Rudio, Denny Tsai

[Project Proposal v.2 (10/29/20)](https://docs.google.com/document/d/1FbrikDlhLAaNADgYI_8JAUBbm_Q2gItGKLAwzME5ZRE/edit?usp=sharing)

## Project Description:
Night Light is a monitoring system for pets/babies that is reliable in many light conditions to detect and report activities of targets in the visual or auditory domain. The system can also execute commands presented by a user interface in real time.

## Objectives/Fulfillments:
- Real time pose tracking daytime nighttime by OpenCv
- Functional feedback after event detected in vision by camera or gesture by IMU
- Real time reaction and execution of commands

## System Description:
Note: Subject to change as project is implemented
### Sensors
**Hardware**
- Night vision camera and regular camera modes (Ideally integrated into one)
- Laptop/Screen
- Phone for external command interface
- Speaker and Microphone (separate)
- IMU on RPi
**Software**
- Python Speech Library (Speech Recognition)
- Python with OpenCV

### Flip Detection
- Accelerometer, gyroscope (6DOF) for IMU orientation and general movement
- IMU measures motion and ports data to central processing, which compares with robust gesture classifiers to a certain tolerance.

### Image Processing
- Use opencv for gathering video data then send to the host.
- Implementation Note: image processing is done in the host machine.

### Graphics/Display
- Streaming option (UDP)
- Interactive menu with options
- App interface (Mobile)

### Commands/Feedback
- Text or Voice based commands to the laptop (TCP)
- Recording option
- Alerts option
- Classification of targets

## Tasks
**Task1:  Sound Processing**
- [x] Filter target audio from background noise (Denny)
- [x] Noise detection (Robert)
- [x] Server/Client audio saving (Robert)
- [x] Semi - Real time audio play with server and client (Robert)
- [x] Create reliable sound classifier (Robert)
- [x] Send notifications on classified sounds (Robert)
- [x] Implement sound database with sound play on command (Robert)

**Task 2: Video** 
- [x] Detect movement outside of a boundary (Henry)
- [x] Implement server client code for streaming video (Henry)
- [x] Motion processing for video stream on server (Henry)
- [x] Classifier processing on client (offload to Rpi) (Henry)
- [ ] Crib Detection
- [ ] Detect pose of the baby relative to crib (sleeping/active)
- [x] End to end video stream connection from rpi to gui (Henry and Denny)

**Task 3: Communications**
- [x] Send information (alerts), Receive commands (Leondi)
- [x] Transmit/Receive Audio files (Robert)
- [x] Send play lullaby command (Robert)

**Task 4: Central Processing**
- [x] Create webserver and ping clients (Robert, Denny, and Henry)
- [x] Implement threading for multiple servers with TCP (Denny and Henry)
- [x] Transmit video from RPI client to GUI laptop via server (Henry)
- [ ] Create main process to run threads [IN PROGRESS]

**Task 5: GUI**
- [x] Create interface with buttons (Leondi)
- [x] Add image display (Leondi)
- [ ] Embed video stream functionality [IN PROGRESS]
- [x] Send and receive user commands with MQTT in event handlers (Leondi and Robert)

**Task 6: IMU**
- [x] Create classifiers for key baby actions (Denny)
- [x] Implement notification in IMU (Denny)

**Task 7: Voice Command** 
- [x] Setup classifiers for voice commands (Leondi)
- [x] Implement event handlers as actions (Henry and Leondi)

**Demo Setup and Run**
Video:

Play Lullaby:

GUI:

IMU:

Voice Command:
