## File Replacer v2.0 (file_replacer.py)
- Replace file based on folder structure
- Support regular expression filtering

## Mouse/Keyboard Input Recorder v3.0 (pynput_recorder.py)
- Record mouse and keyboard actions on Windows and generate a python script
- Support looping

##### Requirement:
- Install pynput library

## whatsapp Chatbot v1.1 (wts_chatbot.py)

##### Requirement:
- Install Google Chrome<br/>
- Install selenium library<br/>
- Download Chrome Driver chromedriver.exe and put in PATH

##### Instruction:
(1) Scan QR code<br/>
(2) Input receiver's name<br/>
(3) Confirm receiver's name<br/>
(4) Press enter to start chatbot

##### Note:
- Support English only
- Press Ctrl+C or close Python Shell to stop chatbot
- Prevent your phone from going to sleep
- Ensure network connectivity

##### Other setting:
default_receiver = 'receiver_name'    #just press enter and program will use it as input name
refresh_interval = 0.5                         #the shorter the refresh time interval, the faster the program can notice a new message
enable_emoji = True                          #set to False if do not want emoji
