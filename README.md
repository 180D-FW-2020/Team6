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
**Software**
- Python Speech Library (Speech Recognition)
- Python with OpenCV

### Object Detection
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
- [x] Filter target audio from background noise
- [x] Server/Client audio saving
- [ ] Real time audio play with server and client

**Task 2: Video** 
- [x] Detect movement outside of a boundary
- [x] Implement server client code for streaming video
- [ ] Motion processing for video stream
- [ ] Detect pose of the baby relative to crib (sleeping/active)

**Task 3: Communications**
- [ ] Send information (alerts), Receive commands
- [ ] Record video
- [ ] Transmit/Receive Audio files

**Task 4: Central Processing**
-[ ] Create webserver and ping clients

**Task 5: GUI**
-[ ] Create interface with buttons
-[ ] Embed video stream functionality
-[ ] Send and receive user commands
