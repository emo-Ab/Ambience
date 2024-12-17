Ambiense House Sound ambience Monitor
--------------------------------------

A blueprint for setting up a smart ambient sound monitoring device for any living/working space. This smart device will monitor
the ambient noise levels in the configured area and lights up to indicate the ambience of the area. Using a mic array, it is
possible to implement complex audio processing algorithms such as speech processing, diametrization, etc.

The target of the project is towards home automation/office automation, in environment where needs of sound sensitive people
may be addresses. Silent zones in libraries, offices, train carriages etc. could be locations where a device could be implemented.
The versatility of Raspberry Pi enables easy customization of the SW to cater to individual applications and environment.

Hardware
--------
1. Raspberry Pi  (https://www.raspberrypi.com/)
2. ReSpeaker 4-mic array (https://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/)


Repository
----------
1. Ambisense (git@github.com:emo-Ab/Ambinent_House.git)

Software Dependency (Device Node)
----------------------
1. Raspberry Pi Os with bullseye Kernel (https://www.raspberrypi.org/downloads/raspbian/) (2021-10-30-raspios-bullseye-arm64)
2. Device Drivers (https://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/)
3. Python (3.10.12)

Installation (Device Node)
------------
1. Install the Raspberry Pi OS on Pi.
2. Follow instructions to connect and install the mic array.
3. Run test application to verify mic array is working.
4. Clone the Ambisense project.
5. Update the settings.json as per connected recording device and web server.
5. Run main.py.

Calibration
-----------
The following functionality may be calibrated by modifying values in the software- 
1. The sensitivity of noise detection
2. Intensity of LED

Software Dependency (Web Server)
---------------------
1. Node.js

Installation (Web Server)
---------------------
1. Copy directory server in Ambisense repository.
2. Set the ip address of the server.
3. Update the web address in the html page.
3. Run webserver_node.js

Simulation and Testing
----------------------
1. The monitor software may be run on PC.
2. Modify the settings.json.

Edge Computing
--------------
Machine learning algorithms may be trained on PC and ported to Raspberry Pi.
Possible applications include voice detection, bark detection, speech detection,
voice diametrization.

References
----------
1. https://github.com/GianlucaPaolocci/Sound-classification-on-Raspberry-Pi-with-Tensorflow
2. https://console.picovoice.ai/
3. https://huggingface.co/dima806/music_genres_classification
4. https://edgeimpulse.com/
