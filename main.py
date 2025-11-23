#system imports
import os
import logging
import json

#logging settings
os.environ["VOSK_LOG_LEVEL"] = "0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('torch').setLevel(logging.ERROR)

#face imports
import cv2
from deepface import DeepFace

#audio imports
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import wave

#ui imports
import textwrap

#global variables
speech_model = Model("./models/vosk-model-small-en-us-0.15")
output_dir = "./output/"
face_input = "./data/faces/"
audio_input = "./data/audio/"
menu_width = 30

#audio speech to text class
class Audio:
    @staticmethod
    def file_input(path):#transcribe from file
        wf = wave.open(path,"rb")
        rec = KaldiRecognizer(speech_model, wf.getframerate())
        text = ""

        while True:
            data = wf.readframes(4000)
            if not data:
                break

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text += result.get("text", "") + " "

        final = json.loads(rec.FinalResult())
        text += final.get("text", "")

        with open(f"{output_dir+text.split()[0]}.json", "a") as f:
            f.write(text.strip())
            f.close()

        return text.strip()

    @staticmethod
    def microphone_input():#transcribe from microphone
        rec = KaldiRecognizer(speech_model, 16000)
        def callback(indata, frames, time, status):
            data = bytes(indata)
            if rec.AcceptWaveform(data):
                full = json.loads(rec.Result())["text"]
                print("\rFinal:" + full + " " * 20, end="", flush=True)
            else:
                partial = json.loads(rec.PartialResult())["partial"]
                print("\rPartial:" + partial + " " * 20, end="", flush=True)

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback,
        ):
            print("Listening... press ctrl+c to quit.")
            try:
                while True:
                    pass
            except KeyboardInterrupt:
                print("\nStopping..")
                clear_screen()

#facial recognition class
class Face:
    @staticmethod
    def file_input(path):#detect from file func
        if not os.path.isfile(path):
            print("File not found")
            return
        img = cv2.imread(path)
        if img is None:
            print("Could not load image")
            return

        detections = DeepFace.extract_faces(img_path=path, detector_backend='opencv', enforce_detection=False)

        for d in detections:
            fa = d["facial_area"]
            x = fa["x"]
            y = fa["y"]
            w = fa["w"]
            h = fa["h"]
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)

        print(f"Found {len(detections)} face(s). Press any key to close image")
        cv2.imshow("Faces", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        clear_screen()

    @staticmethod
    def camera_input():#detect from camera func
        capture = cv2.VideoCapture(0, cv2.CAP_V4L2)
        if not capture.isOpened():
            print("Could not open camera")
            return
        while True:
            ret, frame = capture.read()
            if not ret:
                print("Failed to read frame")
                break

            detections = DeepFace.extract_faces(img_path= frame, detector_backend='opencv', enforce_detection=False)

            for d in detections:
                fa = d["facial_area"]
                x = fa["x"]
                y = fa["y"]
                w = fa["w"]
                h = fa['h']
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

            cv2.imshow("Camera", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            capture.release()
            cv2.destroyAllWindows()
            clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

#facial menu
def face_menu():
    clear_screen()
    title = "Camera & File Facial Detection Menu"
    options = ["[1] Detect from file.", "[2] Detect from camera.", "[b] Return to main menu."]
    while True:
        title_box = textwrap.wrap(title, width=menu_width)
        print("\n+" + "-"*menu_width + "+")
        for line in title_box:
            print("|" + line.center(menu_width) + "|")
        print("+" + "-"*menu_width + "+")

        for entry in options:
            wrapped_lines = textwrap.wrap(entry, width=menu_width)
            for line in wrapped_lines:
                print("|" + line.center(menu_width) + "|")
        print("+" + "-"*menu_width + "+")
        choice = input("Option> ")

        if choice == "1":
            path = input("Enter file name> ")
            Face.file_input(face_input + path)
        elif choice == "2":
            Face.camera_input()
        elif choice.lower() == "b":
            break
        else:
            print("Enter a valid choice.")
    main()

#audio menu
def audio_menu():
    clear_screen()
    title = "Audio Speech to text menu"
    options = ["[1] Transcribe from file.", "[2] Transcribe from microphone.", "[b] Return to main menu."]
    while True:
        title_box = textwrap.wrap(title, width=menu_width)
        print("\n+" + "-"*menu_width + "+")
        for line in title_box:
            print("|" + line.center(menu_width) + "|")
        print("+" + "-"*menu_width + "+")

        for entry in options:
            wrapped_lines = textwrap.wrap(entry, width=menu_width)
            for line in wrapped_lines:
                print("|" + line.center(menu_width) + "|")
        print("+" + "-"*menu_width + "+")

        choice = input("Option> ")
        if choice == "1":
            path = input("Enter file name> ")
            while True:
                if path and os.path.exists(audio_input + path):
                    Audio.file_input(audio_input + path)
                    break
                elif path.lower() == "q":
                    break
                else:
                    print("Enter a valid file name.")
        elif choice == "2":
            Audio.microphone_input()
        elif choice.lower() == "b":
            break
        else:
            print("Enter a valid option.")
    main()

def main():
    clear_screen()
    title = "MultiModel AI Detection"
    options = ["[1] Face Menu.", "[2] Audio Menu.", "[q] Quit"]
    while True:
        title_box = textwrap.wrap(title, width=menu_width)
        print("\n+" + "-"*menu_width + "+")
        for line in title_box:
            print("|" + line.center(menu_width) + "|")
        print("+" + "-"*menu_width + "+")

        for entry in options:
            wrapped_lines = textwrap.wrap(entry, width=menu_width)
            for line in wrapped_lines:
                print("|" + line.center(menu_width) + "|")
        print("+" + "-"*menu_width + "+")
        choice = input("Option> ")

        if choice == "1":
            face_menu()
        elif choice == "2":
            audio_menu()
        elif choice.lower() == "q":
            print("Goodbye")
            exit()
        else:
            print("Enter a valid option.")
    
if __name__ == "__main__":
    print("########################################")
    print("#              DISCLAIMER              #")
    print("#   PLEASE ENSURE ALL INPUT FILES ARE  #")
    print("#     LOCATED IN /data AND IN THEIR    #")
    print("#           RESPECTIVE FOLDERS         #")
    print("########################################")
    if not os.path.exists("./data"):
        os.makedirs("/data")
        os.makedirs("/data/faces")
        os.makedirs("/data/audio")
    
    if not os.path.exists("./output"):
        os.makedirs(output_dir)

    main()
