# Project NightLight
## Team 6: Henry Kou, Leondi Soetojo, Robert Renzo Rudio, Denny Tsai

[Project Report v.4 (2/10/21)](https://docs.google.com/document/d/19eHffGHNeqmLUl1tkrrUShQl4mpEngvESbYaPZqIT5w/edit?usp=sharing)

[NightLight User Manual v.1 (2/10/21)](https://docs.google.com/document/d/1xTz96g2qR92mgjZfghrevOjGbCRnPGg_qQ0c41JhAck/edit?usp=sharing)

## Project Description:
Careful monitoring of your baby is a universal duty for every great parent. But for a lot of people, 
adjusting to parenthood can be challenging when juggling work, pets, family, hobbies, and much more. 
Introducing NightLight, a solution that helps parents securely monitor their infants with a low cost device that has can compete with industry standard technologies.

The NightLight Baby Monitor implements many features:
1. Motion detection with its infrared video stream that operates in all light conditions.
2. Sound classification with an audio stream capable of filtering and recording audio to determine your baby's cries.
3. Instant notifications through email of any suspicious activities from the babyside.
4. Pose recognition from an IMU that updates whenever your baby is standing upright or laying face-up or face-down.
5. Intuitive GUI with encrypted login system and array of commands including playing lullabies and downloading recordings.
5. Voice recognition for hands-free, "Siri-like" commands.

All of these are integrated into a device with real time and secure performance at a low cost. With its competitive abilities, 
the NightLight baby monitor has lots of room to excel in the stable market of infant products.

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
- Streaming video option (Initiate video TCP client)
- Streaming audio option (Initiate adio TCP client)
- Play Lullaby option
- Chat with other remote users option

### Commands/Feedback
- Text or Voice based commands to the laptop (TCP)
- Recording option
- Alerts option
- Classification of targets

### Secure Login
- SQL Local database updates AWS server with encrypted user account info

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
- [x] End to end video stream connection from rpi to gui (Henry and Denny)
- [x] Multiclient video stream (Henry, Denny)
- [x] Reconnect video stream after exiting (Henry)
- [ ] Finish Notifications from RPI Motion classifier (Henry)
- [ ] MQTT email grabber for notifications on RPI (Henry)
- [ ] Embed video into GUI (Henry and Leondi)  [IN PROGRESS]
- [ ] Crib detection classifier (Henry)  [IN PROGRESS]
 
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
- [x] Chat Box between multi client
- [x] User account registering (Leondi)
- [ ] User 
- [x] User login use cases (Leondi)

**Task 6: IMU**
- [x] Create classifiers for key baby actions (Denny)
- [x] Implement notification in IMU (Denny)

**Task 7: Voice Command** 
- [x] Setup classifiers for voice commands (Leondi)
- [x] Implement event handlers as actions (Henry and Leondi)

**Task 8: System**
- [x] Install Script (Robert)
- [x] Running Mac Script (Denny) 
- [x] Running Windows Script (Henry)
