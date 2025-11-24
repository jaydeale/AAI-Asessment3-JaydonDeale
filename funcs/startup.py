#Imports for checking depenencies
import os
import sys
import logging
import subprocess
from .utils import face_input, audio_input, output_dir

#List for required packages
REQUIRED_PACKAGES = [
        "vosk==0.3.45",
        "sounddevice==0.4.9",
        "deepface==0.0.91",
        "tf-keras"
        #"opencv-python==4.8.0.74"
        ]

#Install function for check function
def install(package):
    #subprocess.check_call([sys.executable, "-m","uv" ,"pip", "install", package])
    subprocess.check_call(["uv", "pip", "install", package])
#Check function for depenencies
def check_and_install_packages():
    import importlib
    for pkg in REQUIRED_PACKAGES:#Loop through all required packages
        pkg_name = pkg.split("==")[0]#Get the name of the package
        try:
            importlib.import_module(pkg_name)#Try import the package
        except ImportError:
            print(f"Installing missing packages: {pkg}")#Notify of installation
            install(pkg_name)#Call func with package name to install
try:
    if not os.path.exists("data/"):
        os.makedirs("data/")#Create data
        os.makedirs(face_input)#Create face input folder
        os.makedirs(audio_input)#Create audio input folder
except FileExistsError:
    pass

try:
    #Check if output dir exists
    if not os.path.exists("output/"):
        os.makedirs(output_dir)#Create output folder
except FileExistsError:
    pass

#Set logging information 
os.environ["VOSK_LOG_LEVEL"] = "0" #Set Vosk Logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#Set Deepface Logging
logging.getLogger('torch').setLevel(logging.ERROR)#Set pytorch (deepface depenency) logging



