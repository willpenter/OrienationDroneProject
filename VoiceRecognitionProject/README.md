# Voice-Controlled Drone Project

## Project Overview
This project is designed to control a DJI Tello drone using voice commands. It uses Python scripting with the Vosk library for offline voice recognition, Google Speech Recognition for online voice recognition, and the djitellopy library for drone control. Allows for a hands free, voice activated drone control.

## Key Features
- **Voice Command Recognition**: Uses offline/online voice recognition to interpret and execute drone commands.
- **DJI Tello Drone Control**: 

## Steps to Use
1. Clone the repository
2. Install the dependencies. The dependencies are listed in the requirements.txt file. Run the following command in the 'VoiceRecognitionProject' directory of the project: <br>```cd VoiceRecognitionProject```<br>```pip install -r requirements.txt```
3. Run the online/offline respective file with<br>Online: ```python src/VoiceRecognitionOnline.py```<br>or<br>Offline: ```python src/VoiceRecognitionOffline.py```