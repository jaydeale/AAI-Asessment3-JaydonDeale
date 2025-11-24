╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                       MultiModel AI Detection Tool                       ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                         FIRST STARTUP INSTUCTIONS                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
If you have not run this program before, please run the main.py file. It will
automatically install all of the dependancies required using uv. Future pip 
integration will be implemented. It will also create all of the required 
directories used by this program.

╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                       FILE DETECTION INSTRUCTIONS                        ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
This program supports detecting faces and transcribing audio from files, as 
well as live input from your camera and microphone. To use file input. As 
mentioned before please run the program first to create the necesarry folders.
For all audio files please ensure that they are .wav format, and place them
in the /data/audio folder. When prompted for the name, input the name with 
the file extension as well.
For all face photos place them in the /data/faces folder. The photos can be 
any photo format.

╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                               FILE OUTPUT                                ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
All text output will be placed in the output/ folder. You can change this 
in the funcs/util.py function.

╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║                              MODEL CHOICE                                ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
As of right now, there is no model selection. In the future there will be 
choices between models. To use the speech to text function please place any
model from vosk () in the models/ folder. And then in funcs/voice.py set the 
speech_model variable to the path of the model directory.
