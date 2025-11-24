#imports
import json
import threading
import time
import queue
import wave
import sounddevice as sd 
from vosk import KaldiRecognizer, Model
from .utils import output_dir, clear_screen

speech_model = Model("./models/vosk-model-en-us-0.22-lgraph")

#Audio Class holding all audio functions 
class Audio:
    #Static class for using a file input detection
    @staticmethod
    def file_input(path, output_name):
        try:
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
        except Exception as e:
            print(f"Error: {e}")
    #Static function for using microphone detection
    @staticmethod
    def microphone_input():#transcribe from microphone
        try:
            rec = KaldiRecognizer(speech_model, 16000)#Initialize Speech Recognizer
            last_print = 0
            last_partial = ""

            def callback(indata, frames, time, status):#Function to callback and update data
                import time
                nonlocal last_print, last_partial
                data = bytes(indata)#Convert data to bytes

                if rec.AcceptWaveform(data):#If its complete display the result
                    full = json.loads(rec.Result())["text"]#Load the full result
                    print("\rFinal:" + full + " " * 100, end="", flush=True)#Display the result
                    last_partial = ""
                else:
                    partial = json.loads(rec.PartialResult())["partial"]#If not complete load detected words
                    
                    now = time.time()
                    if partial != last_partial and now - last_print > 0.2:
                        print("\rPartial:" + partial + " " * 100, end="", flush=True)#Display partial detection
                        last_print = now
                        last_partial = partial
            stop = False
            
            def audio_thread():
                #Setup Input Stream
                with sd.RawInputStream(
                    samplerate=16000,
                    blocksize=8000,
                    dtype="int16",
                    channels=1,
                    callback=callback,
                ):
                    while not stop:
                        time.sleep(0.01)

            print("Listening... press q to quit.")#Tell user how to quit
            t = threading.Thread(target=audio_thread)
            t.start()

            try:
                while True:#Loop until Stopped
                    key = input("").strip().lower()
                    if key == "q":
                        break
            finally:
                stop = True
                t.join()
                print("\nStopping..")
                clear_screen()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            clear_screen()#Clear the screen before menu
            return
