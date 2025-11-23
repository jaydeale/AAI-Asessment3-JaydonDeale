#Imports for checking depenencies
import sys
import subprocess

#List for required packages
REQUIRED_PACKAGES = [
        "vosk==0.3.72",
        "sounddevice==0.4.9",
        "deepface==0.0.91",
        "opencv-python==4.8.0.74"
        ]

#Install function for check function
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

#Check function for depenencies
def check_and_install_packages():
    import importlib
    for pkg in REQUIRED_PACKAGES:#Loop through all required packages
        pkg_name = pkg.split("==")[0]#Get the name of the package
        try:
            importlib.import_module(pkg_name)#Try import the package
        except ImportError:
            print(f"Installing missing packages: {pkg}")#Notify of installation
            install(pkg)#Call func with package name to install

#Audio Class holding all audio functions 
class Audio:
    #Static class for using a file input detection
    @staticmethod
    def file_input(path, output_name):
        wf = wave.open(path,"rb")#Open the file 
        rec = KaldiRecognizer(speech_model, wf.getframerate())#Initialize the Voice Recognizer
        text = ""#Empty string to hold output
        #Loop for reading the data
        while True:
            data = wf.readframes(4000)#Get the data from the file
            if not data:#If no data break the loop
                break
            #If theres an acceptable result, add it to text
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())#Get the returned output
                text += result.get("text", "") + " "#Add to text string
        
        final = json.loads(rec.FinalResult())#Get final result
        text += final.get("text", "")#Add final output to text string

        with open(f"{output_dir + output_name}.json", "a") as f:#Open file and save it
            f.write(text.strip())#Write file out
            f.close()#Close file 

        return text.strip()
    #Static function for using microphone detection
    @staticmethod
    def microphone_input():#transcribe from microphone
        rec = KaldiRecognizer(speech_model, 16000)#Initialize Speech Recognizer
        def callback(indata, frames, time, status):#Function to callback and update data
            data = bytes(indata)#Convert data to bytes
            if rec.AcceptWaveform(data):#If its complete display the result
                full = json.loads(rec.Result())["text"]#Load the full result
                print("\rFinal:" + full + " " * 20, end="", flush=True)#Display the result
            else:
                partial = json.loads(rec.PartialResult())["partial"]#If not complete load detected words
                print("\rPartial:" + partial + " " * 20, end="", flush=True)#Display partial detection
        #Setup Input Stream
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            print("Listening... press ctrl+c to quit.")#Tell user how to quit
            try:
                while True:#Loop until Stopped
                    pass
            except KeyboardInterrupt:
                print("\nStopping..")
                clear_screen()#Clear screen

#Static class holding all facial detection functions
class Face:
    #Static function to detect face from file input
    @staticmethod
    def file_input(path):
        if not os.path.isfile(path):#Check if file exists
            print("File not found")
            return
        img = cv2.imread(path)#Read file path and image
        if img is None:#If no image return back
            print("Could not load image")
            return
        #Store all detections in a variable
        detections = DeepFace.extract_faces(img_path=path, detector_backend='opencv', enforce_detection=False)
        #Declare and create points around faces
        for d in detections:
            fa = d["facial_area"]#List storing detection values
            x = fa["x"]#x Axis
            y = fa["y"]#Y Axis
            w = fa["w"]#Width
            h = fa["h"]#Height
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)#Draw Rectangle around face with green color
        print(f"Found {len(detections)} face(s). Press any key to close image") #Inform user of how many detections
        cv2.imshow("Faces", img)#Display image and detections
        cv2.waitKey(0)#Wait for key press to quit
        cv2.destroyAllWindows()#Destroy all windows 
        clear_screen()#Clear screen and return to menu
    #Static function to detected faces from a camera
    @staticmethod
    def camera_input():
        capture = cv2.VideoCapture(0, cv2.CAP_V4L2)#Initialize video capture
        if not capture.isOpened():#Check if camera is opened
            print("Could not open camera")
            return
        while True:#Loop for capturing camera
            ret, frame = capture.read()#Read the camera
            if not ret:#If no data
                print("Failed to read frame")
                break
            #Store live detections in a variable
            detections = DeepFace.extract_faces(img_path= frame, detector_backend='opencv', enforce_detection=False)
            #Declare and create points around faces
            for d in detections:
                fa = d["facial_area"]#List containing detection values
                x = fa["x"]#X Axis
                y = fa["y"]#Y Axis
                w = fa["w"]#Width
                h = fa['h']#Height
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)#Draw rectangle around the face/s

            cv2.imshow("Camera", frame)#Display camera with detections

            if cv2.waitKey(1) & 0xFF == ord('q'):#Check statement to see if q has been pressed
                break

            capture.release()#Deinitialize camera
            cv2.destroyAllWindows()#Close the window
            clear_screen()#Clear screen and return to menu
#Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')#Check if windows or linux

#Facial Detection Menu
def face_menu():
    clear_screen()#Clear screen before displaying menu
    title = "Camera & File Facial Detection Menu"#Set the window title
    options = ["[1] Detect from file.", "[2] Detect from camera.", "[b] Return to main menu."]#Set the options
    while True:#Main Face Menu Loop
        title_box = textwrap.wrap(title, width=menu_width)#Create the title box
        print("\n+" + "-"*menu_width + "+")#Print top line
        for line in title_box:#For loop to get all text for the title box
            print("|" + line.center(menu_width) + "|")#Print items in the center of the box
        print("+" + "-"*menu_width + "+")#Print bottom of title box

        for entry in options:#Loop through options
            wrapped_lines = textwrap.wrap(entry, width=menu_width)#Wrap every entry in options
            for line in wrapped_lines:#For loop to display all options
                print("|" + line.center(menu_width) + "|")#Print options in the center of the box
        print("+" + "-"*menu_width + "+")#Print bottom line of box
        choice = input("Option> ")#Get user input

        if choice == "1":#Check for choice 1
            path = input("Enter file name> ")#Get file path
            Face.file_input(face_input + path)#Call the func to detect faces from file
        elif choice == "2":#Check for choice 2
            Face.camera_input()#Call the func to detect faces from camera
        elif choice.lower() == "b":#Check for choice to go back
            break#Break the loop to return to main menu
        else:#Check for invalid input
            print("Enter a valid choice.")#Print input error
    main()#Return to main menu

#Function to display Audio Menu
def audio_menu():
    clear_screen()#Clear screen before display
    title = "Audio Speech to text menu"#Set menu title
    options = ["[1] Transcribe from file.", "[2] Transcribe from microphone.", "[b] Return to main menu."]#Declare menu options
    while True:#Main audio menu loop
        title_box = textwrap.wrap(title, width=menu_width)#Wrap text for title box
        print("\n+" + "-"*menu_width + "+")#Print top row of box
        for line in title_box:#Loop through title option
            print("|" + line.center(menu_width) + "|")#Display title in center of box
        print("+" + "-"*menu_width + "+")#Print the bottom of title box
        for entry in options:#Loop for entries in options
            wrapped_lines = textwrap.wrap(entry, width=menu_width)#Wrap every entry in options
            for line in wrapped_lines:#Loop through all lines
                print("|" + line.center(menu_width) + "|")#Print options in center of box
        print("+" + "-"*menu_width + "+")#Print bottom line of box
        choice = input("Option> ")#Get user input
        if choice == "1":#Check for choice 1
            path = input("Enter file name> ")#Get file path name
            while True:#Loop for file transcription
                if path and os.path.exists(audio_input + path):#check if file exists
                    output_name = input("Enter output name> ")#Set the output name
                    Audio.file_input(audio_input + path, output_name)#Function call to transcribe from file
                    break#Exit the loop
                elif path.lower() == "q":#Check for quit input
                    break#Exit the loop
                else:#Check for invalid input
                    print("Enter a valid file name.")#Notify the user
        elif choice == "2":#Check for choice 2
            Audio.microphone_input()#Func call to transcribe from microphone
        elif choice.lower() == "b":#Check to return to main menu
            break#Exit the loop
        else:#Check for invalid input
            print("Enter a valid option.")#Notify user
    main()#Return to main menu
#Main function
def main():
    clear_screen()#Clear screen
    title = "MultiModel AI Detection"#Set title
    options = ["[1] Face Menu.", "[2] Audio Menu.", "[q] Quit"]#Set options
    while True:#Main loop for main menu
        title_box = textwrap.wrap(title, width=menu_width)#Wrap the title
        print("\n+" + "-"*menu_width + "+")#Print the first line of the box
        for line in title_box:#For loop for lines in title box
            print("|" + line.center(menu_width) + "|")#Print title in center of box
        print("+" + "-"*menu_width + "+")#Print bottom line of title box
        for entry in options:#For loop for entries in options
            wrapped_lines = textwrap.wrap(entry, width=menu_width)#Wrap the text in options
            for line in wrapped_lines:#For loop for every option in wrapped_lines
                print("|" + line.center(menu_width) + "|")#Print the options in center of the box
        print("+" + "-"*menu_width + "+")#Print bottom line of box
        choice = input("Option> ")#Get user input
        if choice == "1":#Check for first option
            face_menu()#Func call to go to face menu
        elif choice == "2":#Check for second option
            audio_menu()#Func call to go to audio menu
        elif choice.lower() == "q":#Check for third menu
            print("Goodbye")#Notify user its closing
            exit()#Quit the program
        else:#Check for invalid Input
            print("Enter a valid option.")
#Startup init
if __name__ == "__main__":
    #Print disclaimer to help users
    print("########################################")
    print("#              DISCLAIMER              #")
    print("#   PLEASE ENSURE ALL INPUT FILES ARE  #")
    print("#     LOCATED IN /data AND IN THEIR    #")
    print("#           RESPECTIVE FOLDERS         #")
    print("########################################")
    #Initialize global variables
    output_dir = "./output/"
    face_input = "./data/faces/"
    audio_input = "./data/audio/"
    menu_width = 30

    #Start import Initialization
    import os
    import logging

    #Check if required dirs exist
    if not os.path.exists("./data"):
        os.makedirs("/data")#Create data
        os.makedirs(face_input)#Create face input folder
        os.makedirs(audio_input)#Create audio input folder

    #Check if output dir exists
    if not os.path.exists("./output"):
        os.makedirs(output_dir)#Create output folder

    #Set logging information 
    os.environ["VOSK_LOG_LEVEL"] = "0" #Set Vosk Logging
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#Set Deepface Logging
    logging.getLogger('torch').setLevel(logging.ERROR)#Set pytorch (deepface depenency) logging

    #Check or install required packages
    check_and_install_packages()

    #System imports
    import json
    import textwrap

    #Face detection imports
    import cv2
    from deepface import DeepFace

    #Audio detection imports
    from vosk import Model, KaldiRecognizer
    import sounddevice as sd
    import wave

    #Initialize Model
    speech_model = Model("./models/vosk-model-small-en-us-0.15")

    #Start main loop
    main()
